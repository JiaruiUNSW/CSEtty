#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc < 2 || argc > 9) {
        fprintf(stderr, "usage: %s CODE [CODE ...]\n", argv[0]);
        return 1;
    }
    int codes[8];
    for (int i = 1; i < argc; i++) {
        char *end = NULL;
        long value = strtol(argv[i], &end, 10);
        if (*argv[i] == '\0' || *end != '\0' || value < 0 || value > 7) return 1;
        codes[i - 1] = (int)value;
    }
    int count = argc - 1;
    pid_t pids[8];
    int created = 0;
    for (; created < count; created++) {
        pids[created] = fork();
        if (pids[created] < 0) break;
        if (pids[created] == 0) _exit(codes[created]);
    }
    if (created != count) {
        for (int i = 0; i < created; i++) waitpid(pids[i], NULL, 0);
        return 1;
    }
    int histogram[8] = {0};
    for (int i = 0; i < count; i++) {
        int status = 0;
        if (waitpid(pids[i], &status, 0) < 0 || !WIFEXITED(status)) return 1;
        int code = WEXITSTATUS(status);
        if (code < 0 || code > 7) return 1;
        histogram[code]++;
    }
    for (int code = 0; code < 8; code++) {
        if (histogram[code] != 0) printf("status %d count=%d\n", code, histogram[code]);
    }
    printf("children=%d\n", count);
    return 0;
}
