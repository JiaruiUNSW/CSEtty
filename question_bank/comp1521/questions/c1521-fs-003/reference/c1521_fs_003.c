#include <stdio.h>
#include <sys/stat.h>

static int fail(void) { fputs("c1521_fs_003: error\n", stderr); return 1; }

int main(int argc, char **argv) {
    if (argc != 2) return fail();
    struct stat info;
    if (stat(argv[1], &info) < 0) return fail();
    if (S_ISREG(info.st_mode)) printf("regular %lld\n", (long long)info.st_size);
    else if (S_ISDIR(info.st_mode)) puts("directory");
    else puts("other");
    return 0;
}
