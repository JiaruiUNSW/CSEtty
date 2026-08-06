#include <stdio.h>
#include <stdlib.h>

static size_t *solve(const int *values, size_t length, size_t maximum) {
    size_t *counts = calloc(maximum + 1, sizeof *counts);
    if (counts == NULL) exit(1);
    for (size_t i = 0; i < length; i++) counts[(size_t)values[i]]++;
    return counts;
}

int main(int argc, char **argv) {
    if (argc < 2) return 2;
    size_t maximum = (size_t)strtoul(argv[1], NULL, 10);
    size_t length = (size_t)(argc - 2);
    int *values = length == 0 ? NULL : malloc(length * sizeof *values);
    if (length != 0 && values == NULL) return 1;
    for (size_t i = 0; i < length; i++) values[i] = atoi(argv[i + 2]);
    size_t *counts = solve(values, length, maximum);
    int printed = 0;
    for (size_t i = 0; i <= maximum; i++) {
        if (counts[i] != 0) {
            printf("%s%zu=%zu", printed ? " " : "", i, counts[i]);
            printed = 1;
        }
    }
    puts(printed ? "" : "EMPTY");
    free(counts);
    free(values);
    return 0;
}
