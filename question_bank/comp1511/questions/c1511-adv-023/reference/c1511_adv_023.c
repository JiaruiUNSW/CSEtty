#include <stdio.h>

static size_t recursive_tally(const char *text, char target) {
    if (*text == '\0') return 0;
    return (size_t)(*text == target) + recursive_tally(text + 1, target);
}

int main(int argc, char **argv) {
    if (argc != 3 || argv[1][0] == '\0' || argv[1][1] != '\0') return 2;
    printf("%zu\n", recursive_tally(argv[2], argv[1][0]));
    return 0;
}
