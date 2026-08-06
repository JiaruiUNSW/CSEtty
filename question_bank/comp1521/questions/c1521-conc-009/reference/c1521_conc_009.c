#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

static int parse(const char *text, long long *out) {
    char *end = NULL;
    errno = 0;
    long long value = strtoll(text, &end, 10);
    if (errno != 0 || *text == '\0' || *end != '\0') return -1;
    *out = value;
    return 0;
}

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

int main(int argc, char **argv) {
    if (argc != 4) {
        fprintf(stderr, "usage: %s START STEP COUNT\n", argv[0]);
        return 1;
    }
    long long start, step, count_value;
    if (parse(argv[1], &start) < 0 || parse(argv[2], &step) < 0 ||
        parse(argv[3], &count_value) < 0 || count_value < 1 || count_value > 1000) return 1;
    int count = (int)count_value;
    int channel[2];
    if (pipe(channel) < 0) return 1;
    pid_t pid = fork();
    if (pid < 0) return 1;
    if (pid == 0) {
        close(channel[0]);
        for (int i = 0; i < count; i++) {
            long long value = start + (long long)i * step;
            if (transfer(channel[1], &value, sizeof value, 1) < 0) _exit(1);
        }
        close(channel[1]);
        _exit(0);
    }
    close(channel[1]);
    long long sum = 0, minimum = 0, maximum = 0;
    int failed = 0;
    for (int i = 0; i < count; i++) {
        long long value;
        if (transfer(channel[0], &value, sizeof value, 0) < 0) { failed = 1; break; }
        if (i == 0 || value < minimum) minimum = value;
        if (i == 0 || value > maximum) maximum = value;
        sum += value;
    }
    unsigned char extra;
    ssize_t n;
    do { n = read(channel[0], &extra, 1); } while (n < 0 && errno == EINTR);
    if (n != 0) failed = 1;
    close(channel[0]);
    int status = 0;
    if (waitpid(pid, &status, 0) < 0 || !WIFEXITED(status) || WEXITSTATUS(status) != 0) failed = 1;
    if (failed) { fprintf(stderr, "sequence worker failed\n"); return 1; }
    printf("count=%d sum=%lld min=%lld max=%lld\n", count, sum, minimum, maximum);
    return 0;
}
