#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

static int fail(void) { fputs("c1521_fs_004: error\n", stderr); return 1; }

int main(int argc, char **argv) {
    if (argc != 3) return fail();
    char *end = NULL;
    errno = 0;
    long target = strtol(argv[2], &end, 10);
    if (errno || end == argv[2] || *end != '\0' || target < 1) return fail();
    FILE *in = fopen(argv[1], "r");
    if (in == NULL) return fail();
    long line = 1;
    int c;
    int wrote = 0;
    int ended = 0;
    while ((c = fgetc(in)) != EOF) {
        if (line == target) {
            putchar(c);
            wrote = 1;
            if (c == '\n') { ended = 1; break; }
        }
        if (c == '\n') line++;
    }
    if (ferror(in) || fclose(in) != 0) return fail();
    if (wrote && !ended) putchar('\n');
    if (!wrote) puts("NOT FOUND");
    return 0;
}
