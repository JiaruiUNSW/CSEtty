#include <ctype.h>
#include <stdio.h>

static int solve(const char *text, int *value) {
    /* TODO: find and parse the first valid signed decimal token. */
    (void)text;
    (void)value;
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int value = 0;
    if (solve(argv[1], &value)) printf("%d\n", value);
    else puts("NONE");
    return 0;
}
