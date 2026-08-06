#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

static int write_all(int fd, const void *buffer, size_t size) {
    const unsigned char *p = buffer;
    while (size > 0) {
        ssize_t n = write(fd, p, size);
        if (n < 0 && errno == EINTR) continue;
        if (n <= 0) return -1;
        p += (size_t)n;
        size -= (size_t)n;
    }
    return 0;
}

static int read_value(int fd, uint64_t *value) {
    unsigned char *p = (unsigned char *)value;
    size_t left = sizeof *value;
    while (left > 0) {
        ssize_t n = read(fd, p, left);
        if (n < 0 && errno == EINTR) continue;
        if (n < 0) return -1;
        if (n == 0) return left == sizeof *value ? 0 : -1;
        p += (size_t)n;
        left -= (size_t)n;
    }
    return 1;
}

static int scan(const char *path, int output) {
    int fd = open(path, O_RDONLY);
    if (fd < 0) return -1;
    unsigned char buffer[4096];
    uint64_t offset = 0;
    int previous_newline = 0;
    int seen = 0;
    for (;;) {
        ssize_t n = read(fd, buffer, sizeof buffer);
        if (n < 0 && errno == EINTR) continue;
        if (n < 0) { close(fd); return -1; }
        if (n == 0) break;
        for (ssize_t i = 0; i < n; i++, offset++) {
            if (!seen || previous_newline) {
                uint64_t value = offset;
                if (write_all(output, &value, sizeof value) < 0) { close(fd); return -1; }
            }
            seen = 1;
            previous_newline = buffer[i] == '\n';
        }
    }
    return close(fd);
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s FILE\n", argv[0]);
        return 1;
    }
    int channel[2];
    if (pipe(channel) < 0) return 1;
    pid_t pid = fork();
    if (pid < 0) return 1;
    if (pid == 0) {
        close(channel[0]);
        int ok = scan(argv[1], channel[1]);
        close(channel[1]);
        _exit(ok == 0 ? 0 : 1);
    }
    close(channel[1]);
    uint64_t *offsets = NULL;
    size_t count = 0;
    size_t capacity = 0;
    int failed = 0;
    for (;;) {
        uint64_t value;
        int result = read_value(channel[0], &value);
        if (result == 0) break;
        if (result < 0) { failed = 1; break; }
        if (count == capacity) {
            size_t next = capacity == 0 ? 16 : capacity * 2;
            uint64_t *grown = realloc(offsets, next * sizeof *grown);
            if (grown == NULL) { failed = 1; break; }
            offsets = grown;
            capacity = next;
        }
        offsets[count++] = value;
    }
    close(channel[0]);
    int status = 0;
    if (waitpid(pid, &status, 0) < 0 || !WIFEXITED(status) || WEXITSTATUS(status) != 0) failed = 1;
    if (failed) { free(offsets); fprintf(stderr, "line-index worker failed\n"); return 1; }
    printf("lines=%zu\n", count);
    for (size_t i = 0; i < count; i++) printf("%zu:%llu\n", i + 1, (unsigned long long)offsets[i]);
    free(offsets);
    return 0;
}

