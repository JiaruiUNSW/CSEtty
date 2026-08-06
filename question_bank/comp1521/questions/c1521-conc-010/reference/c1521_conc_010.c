#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

struct work { unsigned long long first, last, partial; };

static void *sum_range(void *opaque) {
    struct work *work = opaque;
    unsigned long long total = 0;
    if (work->first <= work->last) {
        for (unsigned long long value = work->first; value <= work->last; value++) total += value;
    }
    work->partial = total;
    return NULL;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s N THREADS\n", argv[0]);
        return 1;
    }
    char *end_n = NULL, *end_t = NULL;
    unsigned long long n = strtoull(argv[1], &end_n, 10);
    long parsed_threads = strtol(argv[2], &end_t, 10);
    if (*argv[1] == '\0' || *end_n != '\0' || n > 1000000 ||
        *argv[2] == '\0' || *end_t != '\0' || parsed_threads < 1 || parsed_threads > 8) return 1;
    int threads = (int)parsed_threads;
    pthread_t ids[8];
    struct work work[8];
    int created = 0;
    for (int i = 0; i < threads; i++) {
        work[i].first = n * (unsigned)i / (unsigned)threads + 1;
        work[i].last = n * (unsigned)(i + 1) / (unsigned)threads;
        work[i].partial = 0;
        if (pthread_create(&ids[i], NULL, sum_range, &work[i]) != 0) break;
        created++;
    }
    if (created != threads) {
        for (int i = 0; i < created; i++) pthread_join(ids[i], NULL);
        return 1;
    }
    int failed = 0;
    for (int i = 0; i < threads; i++) if (pthread_join(ids[i], NULL) != 0) failed = 1;
    if (failed) return 1;
    unsigned long long total = 0;
    for (int i = 0; i < threads; i++) total += work[i].partial;
    printf("sum=%llu\n", total);
    return 0;
}
