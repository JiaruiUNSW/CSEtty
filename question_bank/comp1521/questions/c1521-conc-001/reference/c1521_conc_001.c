#define _POSIX_C_SOURCE 200809L
#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

struct result {
    long long sum;
    unsigned long long count;
    int ok;
};

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

static int read_all(int fd, void *buffer, size_t size) {
    unsigned char *p = buffer;
    while (size > 0) {
        ssize_t n = read(fd, p, size);
        if (n < 0 && errno == EINTR) continue;
        if (n <= 0) return -1;
        p += (size_t)n;
        size -= (size_t)n;
    }
    return 0;
}

static struct result scan_file(const char *path) {
    struct result r = {0, 0, 1};
    int fd = open(path, O_RDONLY);
    if (fd < 0) { r.ok = 0; return r; }
    char token[96];
    size_t used = 0;
    unsigned char buf[4096];
    for (;;) {
        ssize_t n = read(fd, buf, sizeof buf);
        if (n < 0 && errno == EINTR) continue;
        if (n < 0) { r.ok = 0; break; }
        if (n == 0) break;
        for (ssize_t i = 0; i < n; i++) {
            if (isspace(buf[i])) {
                if (used != 0) {
                    token[used] = '\0';
                    char *end = NULL;
                    errno = 0;
                    long long value = strtoll(token, &end, 10);
                    if (errno != 0 || end == token || *end != '\0') r.ok = 0;
                    if (!r.ok) break;
                    r.sum += value;
                    r.count++;
                    used = 0;
                }
            } else if (used + 1 < sizeof token) {
                token[used++] = (char)buf[i];
            } else {
                r.ok = 0;
            }
        }
        if (!r.ok) break;
    }
    if (r.ok && used != 0) {
        token[used] = '\0';
        char *end = NULL;
        errno = 0;
        long long value = strtoll(token, &end, 10);
        if (errno != 0 || end == token || *end != '\0') r.ok = 0;
        else { r.sum += value; r.count++; }
    }
    if (close(fd) < 0) r.ok = 0;
    return r;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s FILE_A FILE_B\n", argv[0]);
        return 1;
    }
    int pipes[2][2];
    pid_t pids[2];
    for (int i = 0; i < 2; i++) {
        if (pipe(pipes[i]) < 0) { perror("pipe"); return 1; }
        pids[i] = -1;
    }
    for (int i = 0; i < 2; i++) {
        pids[i] = fork();
        if (pids[i] < 0) { perror("fork"); return 1; }
        if (pids[i] == 0) {
            for (int j = 0; j < 2; j++) {
                close(pipes[j][0]);
                if (j != i) close(pipes[j][1]);
            }
            struct result r = scan_file(argv[i + 1]);
            int ok = write_all(pipes[i][1], &r, sizeof r);
            close(pipes[i][1]);
            _exit(ok == 0 && r.ok ? 0 : 1);
        }
    }
    for (int i = 0; i < 2; i++) close(pipes[i][1]);
    struct result results[2];
    int failed = 0;
    for (int i = 0; i < 2; i++) {
        if (read_all(pipes[i][0], &results[i], sizeof results[i]) < 0) failed = 1;
        close(pipes[i][0]);
    }
    for (int i = 0; i < 2; i++) {
        int status = 0;
        if (waitpid(pids[i], &status, 0) < 0 || !WIFEXITED(status) ||
            WEXITSTATUS(status) != 0 || !results[i].ok) failed = 1;
    }
    if (failed) {
        fprintf(stderr, "file worker failed\n");
        return 1;
    }
    for (int i = 0; i < 2; i++) {
        printf("%d count=%llu sum=%lld\n", i, results[i].count, results[i].sum);
    }
    return 0;
}

