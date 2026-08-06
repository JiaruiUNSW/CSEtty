#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static int fail(void) { fputs("c1521_fs_005: error\n", stderr); return 1; }

static int number(const char *s, unsigned long long *out) {
    if (*s == '-' || *s == '+') return 0;
    char *end = NULL;
    errno = 0;
    unsigned long long value = strtoull(s, &end, 10);
    if (errno || end == s || *end != '\0') return 0;
    *out = value;
    return 1;
}

int main(int argc, char **argv) {
    unsigned long long offset, length;
    if (argc != 4 || !number(argv[2], &offset) || !number(argv[3], &length) || offset > LLONG_MAX) return fail();
    int fd = open(argv[1], O_RDONLY);
    if (fd < 0) return fail();
    if (lseek(fd, (off_t)offset, SEEK_SET) < 0) { close(fd); return fail(); }
    unsigned char buffer[1024];
    int first = 1;
    while (length > 0) {
        size_t wanted = length < sizeof buffer ? (size_t)length : sizeof buffer;
        ssize_t got = read(fd, buffer, wanted);
        if (got < 0 && errno == EINTR) continue;
        if (got < 0) { close(fd); return fail(); }
        if (got == 0) break;
        for (ssize_t i = 0; i < got; i++) {
            if (!first) putchar(' ');
            printf("%02x", buffer[i]);
            first = 0;
        }
        length -= (unsigned long long)got;
    }
    if (close(fd) < 0) return fail();
    putchar('\n');
    return 0;
}
