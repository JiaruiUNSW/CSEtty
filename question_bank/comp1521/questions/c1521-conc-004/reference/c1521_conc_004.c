#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>

struct part {
    unsigned long long bytes;
    unsigned long long sum;
    unsigned long long weighted;
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

static struct part scan_part(const char *path, off_t start, off_t end) {
    struct part out = {0, 0, 0, 1};
    int fd = open(path, O_RDONLY);
    if (fd < 0) { out.ok = 0; return out; }
    unsigned char buffer[4096];
    off_t position = start;
    while (position < end) {
        size_t wanted = sizeof buffer;
        if ((off_t)wanted > end - position) wanted = (size_t)(end - position);
        ssize_t n = pread(fd, buffer, wanted, position);
        if (n < 0 && errno == EINTR) continue;
        if (n <= 0) { out.ok = 0; break; }
        for (ssize_t j = 0; j < n; j++) {
            unsigned long long byte = buffer[j];
            unsigned long long offset = (unsigned long long)(position + j);
            out.bytes++;
            out.sum += byte;
            out.weighted += byte * (offset + 1);
        }
        position += n;
    }
    if (close(fd) < 0) out.ok = 0;
    return out;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s FILE WORKERS\n", argv[0]);
        return 1;
    }
    char *end = NULL;
    long workers_long = strtol(argv[2], &end, 10);
    if (*argv[2] == '\0' || *end != '\0' || workers_long < 1 || workers_long > 8) return 1;
    int workers = (int)workers_long;
    int inspect = open(argv[1], O_RDONLY);
    if (inspect < 0) { perror("open"); return 1; }
    struct stat metadata;
    if (fstat(inspect, &metadata) < 0 || !S_ISREG(metadata.st_mode) || close(inspect) < 0) {
        fprintf(stderr, "input must be a regular file\n");
        return 1;
    }
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
            off_t start = metadata.st_size * i / workers;
            off_t finish = metadata.st_size * (i + 1) / workers;
            struct part out = scan_part(argv[1], start, finish);
            int sent = transfer(channels[i][1], &out, sizeof out, 1);
            close(channels[i][1]);
            _exit(sent == 0 && out.ok ? 0 : 1);
        }
    }
    for (int i = 0; i < workers; i++) close(channels[i][1]);
    struct part total = {0, 0, 0, 1};
    for (int i = 0; i < workers; i++) {
        struct part value;
        if (transfer(channels[i][0], &value, sizeof value, 0) < 0 || !value.ok) total.ok = 0;
        else {
            total.bytes += value.bytes;
            total.sum += value.sum;
            total.weighted += value.weighted;
        }
        close(channels[i][0]);
    }
    for (int i = 0; i < workers; i++) {
        int status = 0;
        if (waitpid(pids[i], &status, 0) < 0 || !WIFEXITED(status) || WEXITSTATUS(status) != 0) total.ok = 0;
    }
    if (!total.ok) { fprintf(stderr, "chunk worker failed\n"); return 1; }
    printf("bytes=%llu sum=%llu weighted=%llu\n", total.bytes, total.sum, total.weighted);
    return 0;
}

