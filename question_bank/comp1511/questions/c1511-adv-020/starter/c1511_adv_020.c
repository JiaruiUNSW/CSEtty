#include <stdio.h>
#include <stdlib.h>

static char *vowel_trace(const char *text) {
    // TODO: allocate and return the vowel-only string.
    (void)text;
    char *result = malloc(1);
    if (result == NULL)
        exit(1);
    result[0] = '\0';
    return result;
}

int main(int argc, char **argv) {
    if (argc != 2)
        return 2;
    char *result = vowel_trace(argv[1]);
    puts(result);
    free(result);
    return 0;
}
