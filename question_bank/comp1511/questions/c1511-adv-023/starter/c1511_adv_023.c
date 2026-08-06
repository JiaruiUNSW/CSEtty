#include <stdio.h>

static size_t solve(const char *text, char target) {
    /* TODO: recursively tally target in text. */
    (void)text;
    (void)target;
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 3 || argv[1][0] == '\0' || argv[1][1] != '\0') return 2;
    printf("%zu\n", solve(argv[2], argv[1][0]));
    return 0;
}
