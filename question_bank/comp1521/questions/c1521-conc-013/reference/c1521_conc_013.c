#define _POSIX_C_SOURCE 200809L
#include <ctype.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ACCOUNTS 64
struct operation { char account[32]; long long delta; };
struct account { char name[32]; long long balance; };
struct ledger { struct account accounts[MAX_ACCOUNTS]; int count; pthread_mutex_t mutex; };
struct job { struct operation *ops; size_t count, start, stride; struct ledger *ledger; int failed; };

static int valid_name(const char *name) {
    if (*name == '\0') return 0;
    for (const unsigned char *p=(const unsigned char *)name; *p; p++) {
        if (!islower(*p) && !isdigit(*p)) return 0;
    }
    return 1;
}

static void *apply_operations(void *opaque) {
    struct job *job = opaque;
    for (size_t i = job->start; i < job->count; i += job->stride) {
        if (pthread_mutex_lock(&job->ledger->mutex) != 0) { job->failed = 1; return NULL; }
        int found = -1;
        for (int j = 0; j < job->ledger->count; j++) {
            if (strcmp(job->ledger->accounts[j].name, job->ops[i].account) == 0) found = j;
        }
        if (found < 0) {
            if (job->ledger->count == MAX_ACCOUNTS) {
                job->failed = 1;
                pthread_mutex_unlock(&job->ledger->mutex);
                return NULL;
            }
            found = job->ledger->count++;
            strcpy(job->ledger->accounts[found].name, job->ops[i].account);
            job->ledger->accounts[found].balance = 0;
        }
        job->ledger->accounts[found].balance += job->ops[i].delta;
        if (pthread_mutex_unlock(&job->ledger->mutex) != 0) { job->failed = 1; return NULL; }
    }
    return NULL;
}

static int compare_accounts(const void *a, const void *b) {
    const struct account *left = a, *right = b;
    return strcmp(left->name, right->name);
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s FILE THREADS\n", argv[0]);
        return 1;
    }
    char *end = NULL;
    long parsed = strtol(argv[2], &end, 10);
    if (*argv[2] == '\0' || *end != '\0' || parsed < 1 || parsed > 8) return 1;
    FILE *input = fopen(argv[1], "r");
    if (input == NULL) return 1;
    struct operation *ops = NULL;
    size_t count = 0, capacity = 0;
    char *line = NULL;
    size_t line_capacity = 0;
    ssize_t length;
    int failed = 0;
    while ((length = getline(&line, &line_capacity, input)) >= 0) {
        int only_space = 1;
        for (ssize_t i = 0; i < length; i++) if (!isspace((unsigned char)line[i])) only_space = 0;
        if (only_space) continue;
        struct operation op;
        char extra;
        if (sscanf(line, "%31s %lld %c", op.account, &op.delta, &extra) != 2 || !valid_name(op.account)) { failed = 1; break; }
        if (count == capacity) {
            size_t next = capacity == 0 ? 32 : capacity * 2;
            struct operation *grown = realloc(ops, next * sizeof *grown);
            if (grown == NULL) { failed = 1; break; }
            ops = grown;
            capacity = next;
        }
        ops[count++] = op;
        if (count > 1000) { failed = 1; break; }
    }
    if (ferror(input) || fclose(input) != 0) failed = 1;
    free(line);
    if (failed) { free(ops); return 1; }
    int threads = (int)parsed;
    struct ledger ledger = {.count=0, .mutex=PTHREAD_MUTEX_INITIALIZER};
    pthread_t ids[8];
    struct job jobs[8];
    int created = 0;
    for (int i = 0; i < threads; i++) {
        jobs[i] = (struct job){ops,count,(size_t)i,(size_t)threads,&ledger,0};
        if (pthread_create(&ids[i],NULL,apply_operations,&jobs[i]) != 0) break;
        created++;
    }
    failed = created != threads;
    for (int i = 0; i < created; i++) if (pthread_join(ids[i],NULL) != 0 || jobs[i].failed) failed = 1;
    if (!failed) {
        qsort(ledger.accounts,(size_t)ledger.count,sizeof ledger.accounts[0],compare_accounts);
        for (int i = 0; i < ledger.count; i++) printf("%s=%lld\n",ledger.accounts[i].name,ledger.accounts[i].balance);
    }
    if (pthread_mutex_destroy(&ledger.mutex) != 0) failed = 1;
    free(ops);
    return failed ? 1 : 0;
}
