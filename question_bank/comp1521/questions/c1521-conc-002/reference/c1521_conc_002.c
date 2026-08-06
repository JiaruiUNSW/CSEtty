#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

struct fingerprint { unsigned long long bytes; unsigned checksum; int ok; };

static int transfer(int fd, void *buffer, size_t size, int writing) {
    unsigned char *p = buffer;
    while (size != 0) {
        ssize_t n = writing ? write(fd, p, size) : read(fd, p, size);
        if (n < 0 && errno == EINTR) continue;
        if (n <= 0) return -1;
        p += (size_t)n;
        size -= (size_t)n;
    }
    return 0;
}

static struct fingerprint fingerprint(const char *path) {
    struct fingerprint out = {0, 0, 1};
    int fd = open(path, O_RDONLY);
    if (fd < 0) { out.ok = 0; return out; }
    unsigned char buffer[4096];
    for (;;) {
        ssize_t n = read(fd, buffer, sizeof buffer);
        if (n < 0 && errno == EINTR) continue;
        if (n < 0) { out.ok = 0; break; }
        if (n == 0) break;
        for (ssize_t i = 0; i < n; i++) {
            out.checksum = (out.checksum + buffer[i]) & 0xffffu;
            out.bytes++;
        }
    }
    if (close(fd) < 0) out.ok = 0;
    return out;
}

int main(int argc, char **argv) {
    if (argc < 2 || argc > 5) {
        fprintf(stderr, "usage: %s FILE [FILE ...]\n", argv[0]);
        return 1;
    }
    int count = argc - 1;
    int channels[4][2];
    pid_t pids[4];
    for (int i = 0; i < count; i++) {
        if (pipe(channels[i]) < 0) { perror("pipe"); return 1; }
    }
    for (int i = 0; i < count; i++) {
        pids[i] = fork();
        if (pids[i] < 0) { perror("fork"); return 1; }
        if (pids[i] == 0) {
            for (int j = 0; j < count; j++) {
                close(channels[j][0]);
                if (j != i) close(channels[j][1]);
            }
            struct fingerprint out = fingerprint(argv[i + 1]);
            int status = transfer(channels[i][1], &out, sizeof out, 1);
            close(channels[i][1]);
            _exit(status == 0 && out.ok ? 0 : 1);
        }
    }
    for (int i = 0; i < count; i++) close(channels[i][1]);
    struct fingerprint values[4];
    int failed = 0;
    for (int i = 0; i < count; i++) {
        if (transfer(channels[i][0], &values[i], sizeof values[i], 0) < 0) failed = 1;
        close(channels[i][0]);
    }
    for (int i = 0; i < count; i++) {
        int status = 0;
        if (waitpid(pids[i], &status, 0) < 0 || !WIFEXITED(status) ||
            WEXITSTATUS(status) != 0 || !values[i].ok) failed = 1;
    }
    if (failed) { fprintf(stderr, "fingerprint worker failed\n"); return 1; }
    for (int i = 0; i < count; i++) {
        printf("%d bytes=%llu checksum=%u\n", i, values[i].bytes, values[i].checksum);
    }
    return 0;
}

