#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

static int parse_value(const char *text, long *out) {
    char *end = NULL;
    long value = strtol(text, &end, 10);
    if (*text == '\0' || *end != '\0' || value < -10000 || value > 10000) return -1;
    *out = value;
    return 0;
}

int main(int argc, char **argv) {
    if (argc == 3 && strcmp(argv[1], "--worker") == 0) {
        long value;
        if (parse_value(argv[2], &value) < 0) return 1;
        printf("%ld\n", value * value);
        return 0;
    }
    if (argc < 2 || argc > 7) {
        fprintf(stderr, "usage: %s VALUE [VALUE ...]\n", argv[0]);
        return 1;
    }
    int count = argc - 1;
    long values[6];
    for (int i = 0; i < count; i++) if (parse_value(argv[i + 1], &values[i]) < 0) return 1;
    int channels[6][2];
    pid_t pids[6];
    for (int i = 0; i < count; i++) if (pipe(channels[i]) < 0) return 1;
    for (int i = 0; i < count; i++) {
        pids[i] = fork();
        if (pids[i] < 0) return 1;
        if (pids[i] == 0) {
            if (dup2(channels[i][1], STDOUT_FILENO) < 0) _exit(127);
            for (int j = 0; j < count; j++) {
                close(channels[j][0]);
                close(channels[j][1]);
            }
            execl(argv[0], argv[0], "--worker", argv[i + 1], (char *)NULL);
            _exit(127);
        }
    }
    for (int i = 0; i < count; i++) close(channels[i][1]);
    long squares[6];
    int failed = 0;
    for (int i = 0; i < count; i++) {
        FILE *stream = fdopen(channels[i][0], "r");
        if (stream == NULL || fscanf(stream, "%ld", &squares[i]) != 1) failed = 1;
        if (stream != NULL) fclose(stream); else close(channels[i][0]);
    }
    for (int i = 0; i < count; i++) {
        int status = 0;
        if (waitpid(pids[i], &status, 0) < 0 || !WIFEXITED(status) || WEXITSTATUS(status) != 0) failed = 1;
    }
    if (failed) { fprintf(stderr, "exec worker failed\n"); return 1; }
    for (int i = 0; i < count; i++) printf("%d square=%ld\n", i, squares[i]);
    return 0;
}
