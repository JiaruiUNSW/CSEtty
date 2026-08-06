#include <stdio.h>
#include <stdlib.h>

static int is_vowel(char c) {
    return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u'
        || c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U';
}

static char *solve(const char *text) {
    size_t count = 0;
    for (const char *p = text; *p != '\0'; p++) if (is_vowel(*p)) count++;
    char *result = malloc(count + 1);
    if (result == NULL) exit(1);
    size_t write = 0;
    for (const char *p = text; *p != '\0'; p++) if (is_vowel(*p)) result[write++] = *p;
    result[write] = '\0';
    return result;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *result = solve(argv[1]);
    puts(result);
    free(result);
    return 0;
}
