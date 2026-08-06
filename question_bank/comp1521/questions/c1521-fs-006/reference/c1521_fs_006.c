#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

static int fail(void) { fputs("c1521_fs_006: error\n", stderr); return 1; }

int main(int argc, char **argv) {
    if (argc != 3 || argv[2][0] == '-' || argv[2][0] == '+') return fail();
    char *end = NULL;
    errno = 0;
    unsigned long long width = strtoull(argv[2], &end, 10);
    if (errno || end == argv[2] || *end != '\0' || width == 0) return fail();
    struct stat info;
    if (stat(argv[1], &info) < 0 || !S_ISREG(info.st_mode) || info.st_size < 0) return fail();
    unsigned long long size = (unsigned long long)info.st_size;
    printf("records=%llu trailing=%llu\n", size / width, size % width);
    return 0;
}
