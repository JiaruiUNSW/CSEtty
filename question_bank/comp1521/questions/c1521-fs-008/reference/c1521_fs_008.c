#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

static int fail(void) { fputs("c1521_fs_008: error\n", stderr); return 1; }

int main(int argc, char **argv) {
    if (argc != 2 || argv[1][0] == '-' || argv[1][0] == '+') return fail();
    char *end = NULL;
    errno = 0;
    unsigned long long cp = strtoull(argv[1], &end, 10);
    if (errno || end == argv[1] || *end != '\0') return fail();
    if (cp > 0x10ffff || (cp >= 0xd800 && cp <= 0xdfff)) { puts("invalid"); return 0; }
    unsigned char b[4];
    int n;
    if (cp <= 0x7f) { b[0] = (unsigned char)cp; n = 1; }
    else if (cp <= 0x7ff) { b[0] = 0xc0 | (cp >> 6); b[1] = 0x80 | (cp & 0x3f); n = 2; }
    else if (cp <= 0xffff) { b[0] = 0xe0 | (cp >> 12); b[1] = 0x80 | ((cp >> 6) & 0x3f); b[2] = 0x80 | (cp & 0x3f); n = 3; }
    else { b[0] = 0xf0 | (cp >> 18); b[1] = 0x80 | ((cp >> 12) & 0x3f); b[2] = 0x80 | ((cp >> 6) & 0x3f); b[3] = 0x80 | (cp & 0x3f); n = 4; }
    for (int i = 0; i < n; i++) printf("%s%02x", i ? " " : "", b[i]);
    putchar('\n');
    return 0;
}
