#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>

struct shared { unsigned long long counts[26]; pthread_mutex_t mutex; };
struct job { const char *text; struct shared *shared; int failed; };

static int letter_index(unsigned char c) {
    if (c >= 'A' && c <= 'Z') c = (unsigned char)(c - 'A' + 'a');
    return c >= 'a' && c <= 'z' ? c - 'a' : -1;
}

static void *count_letters(void *opaque) {
    struct job *job = opaque;
    for (const unsigned char *p = (const unsigned char *)job->text; *p; p++) {
        int index = letter_index(*p);
        if (index < 0) continue;
        if (pthread_mutex_lock(&job->shared->mutex) != 0) { job->failed = 1; return NULL; }
        job->shared->counts[index]++;
        if (pthread_mutex_unlock(&job->shared->mutex) != 0) { job->failed = 1; return NULL; }
    }
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 2 || argc > 9) {
        fprintf(stderr, "usage: %s STRING [STRING ...]\n", argv[0]);
        return 1;
    }
    struct shared shared = {{0}, PTHREAD_MUTEX_INITIALIZER};
    int count = argc - 1;
    pthread_t threads[8];
    struct job jobs[8];
    int created = 0;
    for (int i = 0; i < count; i++) {
        jobs[i] = (struct job){argv[i + 1], &shared, 0};
        if (pthread_create(&threads[i], NULL, count_letters, &jobs[i]) != 0) break;
        created++;
    }
    int failed = created != count;
    for (int i = 0; i < created; i++) {
        if (pthread_join(threads[i], NULL) != 0 || jobs[i].failed) failed = 1;
    }
    if (!failed) {
        for (int i = 0; i < 26; i++) if (shared.counts[i] != 0) printf("%c=%llu\n", 'a' + i, shared.counts[i]);
    }
    if (pthread_mutex_destroy(&shared.mutex) != 0) failed = 1;
    return failed ? 1 : 0;
}
