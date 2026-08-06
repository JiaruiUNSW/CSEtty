#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int hd(char c) { if (c >= '0' && c <= '9') return c - '0'; if (c >= 'a' && c <= 'f') return c - 'a' + 10; if (c >= 'A' && c <= 'F') return c - 'A' + 10; return -1; }
static int ct(unsigned char b) { return b >= 0x80 && b <= 0xbf; }
static size_t width(const unsigned char *b, size_t n) {
    if (n && b[0] <= 0x7f) return 1;
    if (n >= 2 && b[0] >= 0xc2 && b[0] <= 0xdf && ct(b[1])) return 2;
    if (n >= 3 && b[0] >= 0xe0 && b[0] <= 0xef && ct(b[2]) && ((b[0] == 0xe0 && b[1] >= 0xa0 && b[1] <= 0xbf) || (b[0] == 0xed && b[1] >= 0x80 && b[1] <= 0x9f) || (b[0] != 0xe0 && b[0] != 0xed && ct(b[1])))) return 3;
    if (n >= 4 && b[0] >= 0xf0 && b[0] <= 0xf4 && ct(b[2]) && ct(b[3]) && ((b[0] == 0xf0 && b[1] >= 0x90 && b[1] <= 0xbf) || (b[0] == 0xf4 && b[1] >= 0x80 && b[1] <= 0x8f) || (b[0] >= 0xf1 && b[0] <= 0xf3 && ct(b[1])))) return 4;
    return 0;
}
int main(int argc, char **argv) {
    if (argc != 2 || strlen(argv[1]) % 2) { fputs("c1521_fs_010: error\n", stderr); return 1; }
    size_t n = strlen(argv[1]) / 2;
    unsigned char *b = malloc(n ? n : 1); size_t *starts = malloc((n ? n : 1) * sizeof *starts); size_t *widths = malloc((n ? n : 1) * sizeof *widths);
    if (!b || !starts || !widths) { free(b); free(starts); free(widths); fputs("c1521_fs_010: error\n", stderr); return 1; }
    for (size_t i = 0; i < n; i++) { int h = hd(argv[1][2*i]), l = hd(argv[1][2*i+1]); if (h < 0 || l < 0) { free(b); free(starts); free(widths); fputs("c1521_fs_010: error\n", stderr); return 1; } b[i] = h * 16 + l; }
    size_t at = 0, count = 0;
    while (at < n) { size_t w = width(b + at, n - at); if (!w) { printf("invalid %zu\n", at); free(b); free(starts); free(widths); return 0; } starts[count] = at; widths[count++] = w; at += w; }
    while (count > 0) { count--; for (size_t j = 0; j < widths[count]; j++) printf("%02x", b[starts[count] + j]); }
    putchar('\n'); free(b); free(starts); free(widths); return 0;
}
