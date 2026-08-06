#include <stdio.h>
#include <stdlib.h>

static char *solve(const char *text) {
    /* TODO: allocate and return the vowel-only string. */
    (void)text;
    char *result = malloc(1);
    if (result == NULL) exit(1);
    result[0] = '\0';
    return result;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *result = solve(argv[1]);
    puts(result);
    free(result);
    return 0;
}
