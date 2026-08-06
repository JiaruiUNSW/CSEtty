#define _POSIX_C_SOURCE 200809L
#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

struct counts {
    unsigned long long lines;
    unsigned long long bytes;
    unsigned long long words;
    int ok;
};

static int transfer(int fd, void *buffer, size_t size, int writing) {
    unsigned char *p = buffer;
    while (size > 0) {
        ssize_t n = writing ? write(fd, p, size) : read(fd, p, size);
        if (n < 0 && errno == EINTR) continue;
        if (n <= 0) return -1;
        p += (size_t)n;
        size -= (size_t)n;
    }
    return 0;
}

static struct counts scan(const char *path, int index, int workers) {
    struct counts out = {0, 0, 0, 1};
    FILE *input = fopen(path, "r");
    if (input == NULL) { out.ok = 0; return out; }
    char *line = NULL;
    size_t capacity = 0;
    ssize_t length;
    unsigned long long line_number = 0;
    while ((length = getline(&line, &capacity, input)) >= 0) {
        if ((int)(line_number % (unsigned)workers) == index) {
            size_t content = (size_t)length;
            if (content > 0 && line[content - 1] == '\n') content--;
            out.lines++;
            out.bytes += content;
            int in_word = 0;
            for (size_t i = 0; i < content; i++) {
                int space = isspace((unsigned char)line[i]);
                if (!space && !in_word) out.words++;
                in_word = !space;
            }
        }
        line_number++;
    }
    if (ferror(input)) out.ok = 0;
    free(line);
    if (fclose(input) != 0) out.ok = 0;
    return out;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s FILE WORKERS\n", argv[0]);
        return 1;
    }
    char *end = NULL;
    long parsed = strtol(argv[2], &end, 10);
    if (*argv[2] == '\0' || *end != '\0' || parsed < 1 || parsed > 8) return 1;
    int workers = (int)parsed;
    int channels[8][2];
    pid_t pids[8];
    for (int i = 0; i < workers; i++) if (pipe(channels[i]) < 0) return 1;
    for (int i = 0; i < workers; i++) {
        pids[i] = fork();
        if (pids[i] < 0) return 1;
        if (pids[i] == 0) {
            for (int j = 0; j < workers; j++) {
                close(channels[j][0]);
                if (j != i) close(channels[j][1]);
            }
            struct counts out = scan(argv[1], i, workers);
            int sent = transfer(channels[i][1], &out, sizeof out, 1);
            close(channels[i][1]);
            _exit(sent == 0 && out.ok ? 0 : 1);
        }
    }
    for (int i = 0; i < workers; i++) close(channels[i][1]);
    struct counts values[8];
    int failed = 0;
    for (int i = 0; i < workers; i++) {
        if (transfer(channels[i][0], &values[i], sizeof values[i], 0) < 0 || !values[i].ok) failed = 1;
        close(channels[i][0]);
    }
    for (int i = 0; i < workers; i++) {
        int status = 0;
        if (waitpid(pids[i], &status, 0) < 0 || !WIFEXITED(status) || WEXITSTATUS(status) != 0) failed = 1;
    }
    if (failed) { fprintf(stderr, "manifest worker failed\n"); return 1; }
    struct counts total = {0, 0, 0, 1};
    for (int i = 0; i < workers; i++) {
        printf("worker %d lines=%llu bytes=%llu words=%llu\n", i, values[i].lines, values[i].bytes, values[i].words);
        total.lines += values[i].lines;
        total.bytes += values[i].bytes;
        total.words += values[i].words;
    }
    printf("total lines=%llu bytes=%llu words=%llu\n", total.lines, total.bytes, total.words);
    return 0;
}

