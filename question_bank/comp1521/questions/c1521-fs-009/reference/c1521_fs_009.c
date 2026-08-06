#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int hex_digit(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    return -1;
}
static int cont(unsigned char b) { return b >= 0x80 && b <= 0xbf; }
static size_t sequence(const unsigned char *b, size_t n) {
    if (n && b[0] <= 0x7f) return 1;
    if (n >= 2 && b[0] >= 0xc2 && b[0] <= 0xdf && cont(b[1])) return 2;
    if (n >= 3 && b[0] >= 0xe0 && b[0] <= 0xef && cont(b[2])) {
        if ((b[0] == 0xe0 && b[1] >= 0xa0 && b[1] <= 0xbf) ||
            (b[0] == 0xed && b[1] >= 0x80 && b[1] <= 0x9f) ||
            (b[0] != 0xe0 && b[0] != 0xed && cont(b[1]))) return 3;
    }
    if (n >= 4 && b[0] >= 0xf0 && b[0] <= 0xf4 && cont(b[2]) && cont(b[3])) {
        if ((b[0] == 0xf0 && b[1] >= 0x90 && b[1] <= 0xbf) ||
            (b[0] == 0xf4 && b[1] >= 0x80 && b[1] <= 0x8f) ||
            (b[0] >= 0xf1 && b[0] <= 0xf3 && cont(b[1]))) return 4;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) { fputs("c1521_fs_009: error\n", stderr); return 1; }
    size_t chars = strlen(argv[1]);
    if (chars % 2 != 0) { fputs("c1521_fs_009: error\n", stderr); return 1; }
    size_t n = chars / 2;
    unsigned char *bytes = malloc(n ? n : 1);
    if (bytes == NULL) { fputs("c1521_fs_009: error\n", stderr); return 1; }
    for (size_t i = 0; i < n; i++) {
        int hi = hex_digit(argv[1][2 * i]), lo = hex_digit(argv[1][2 * i + 1]);
        if (hi < 0 || lo < 0) { free(bytes); fputs("c1521_fs_009: error\n", stderr); return 1; }
        bytes[i] = (unsigned char)(hi * 16 + lo);
    }
    size_t at = 0, count = 0;
    while (at < n) {
        size_t width = sequence(bytes + at, n - at);
        if (width == 0) { printf("invalid %zu\n", at); free(bytes); return 0; }
        at += width; count++;
    }
    printf("valid %zu\n", count);
    free(bytes);
    return 0;
}
