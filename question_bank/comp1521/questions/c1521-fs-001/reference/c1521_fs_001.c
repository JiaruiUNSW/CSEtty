#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static int fail(void) {
    fputs("c1521_fs_001: error\n", stderr);
    return 1;
}

int main(int argc, char **argv) {
    if (argc != 3) return fail();
    char *end = NULL;
    errno = 0;
    long value = strtol(argv[2], &end, 10);
    if (errno != 0 || *argv[2] == '\0' || *end != '\0' || value < 0 || value > 255) return fail();
    int fd = open(argv[1], O_RDONLY);
    if (fd < 0) return fail();
    unsigned char buffer[4096];
    uint64_t count = 0;
    for (;;) {
        ssize_t n = read(fd, buffer, sizeof buffer);
        if (n < 0 && errno == EINTR) continue;
        if (n < 0) { close(fd); return fail(); }
        if (n == 0) break;
        for (ssize_t i = 0; i < n; i++) if (buffer[i] == (unsigned char)value) count++;
    }
    if (close(fd) < 0) return fail();
    printf("%llu\n", (unsigned long long)count);
    return 0;
}
