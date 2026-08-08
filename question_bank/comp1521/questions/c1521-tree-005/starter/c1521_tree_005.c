#define _POSIX_C_SOURCE 200809L

#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

struct summary {
    long long files;
    long long bytes;
    long long depth;
    long long text;
    long long dirs;
    long long largest;
    long long sources;
};

static int walk(const char *path, int depth, struct summary *summary) {
    // TODO: Recursively walk this directory and update summary.
    (void)path;
    (void)depth;
    (void)summary;
    return -1;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        return 1;
    }

    struct summary s = {0};
    if (walk(argv[1], 0, &s) != 0) {
        return 1;
    }

    printf("result: %lld\n", (long long)(s.dirs));
    return 0;
}
