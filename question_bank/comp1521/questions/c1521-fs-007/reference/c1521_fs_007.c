#include <stdio.h>

static int continuation(int value) { return value >= 0x80 && value <= 0xbf; }

int main(void) {
    unsigned long long count = 0;
    int a;
    while ((a = getchar()) != EOF) {
        int b, c, d;
        if (a <= 0x7f) {
        } else if (a >= 0xc2 && a <= 0xdf) {
            b = getchar();
            if (!continuation(b)) { puts("invalid"); return 0; }
        } else if (a >= 0xe0 && a <= 0xef) {
            b = getchar(); c = getchar();
            int second = (a == 0xe0) ? (b >= 0xa0 && b <= 0xbf)
                       : (a == 0xed) ? (b >= 0x80 && b <= 0x9f) : continuation(b);
            if (!second || !continuation(c)) { puts("invalid"); return 0; }
        } else if (a >= 0xf0 && a <= 0xf4) {
            b = getchar(); c = getchar(); d = getchar();
            int second = (a == 0xf0) ? (b >= 0x90 && b <= 0xbf)
                       : (a == 0xf4) ? (b >= 0x80 && b <= 0x8f) : continuation(b);
            if (!second || !continuation(c) || !continuation(d)) { puts("invalid"); return 0; }
        } else {
            puts("invalid");
            return 0;
        }
        count++;
    }
    if (ferror(stdin)) { fputs("c1521_fs_007: error\n", stderr); return 1; }
    printf("%llu\n", count);
    return 0;
}
