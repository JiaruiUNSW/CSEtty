#define _POSIX_C_SOURCE 200809L
#include <ctype.h>
#include <pthread.h>
#include <stdio.h>

struct job { const char *text; unsigned long long vowels; };

static void *count_vowels(void *opaque) {
    struct job *job = opaque;
    for (const unsigned char *p = (const unsigned char *)job->text; *p; p++) {
        int c = tolower(*p);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') job->vowels++;
    }
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 2 || argc > 9) {
        fprintf(stderr, "usage: %s STRING [STRING ...]\n", argv[0]);
        return 1;
    }
    int count = argc - 1;
    pthread_t threads[8];
    struct job jobs[8];
    int created = 0;
    for (int i = 0; i < count; i++) {
        jobs[i].text = argv[i + 1];
        jobs[i].vowels = 0;
        if (pthread_create(&threads[i], NULL, count_vowels, &jobs[i]) != 0) break;
        created++;
    }
    int failed = created != count;
    for (int i = 0; i < created; i++) if (pthread_join(threads[i], NULL) != 0) failed = 1;
    if (failed) return 1;
    for (int i = 0; i < count; i++) printf("%d vowels=%llu\n", i, jobs[i].vowels);
    return 0;
}
