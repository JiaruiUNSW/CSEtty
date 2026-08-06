#include <stdio.h>
#include <stdlib.h>

static void solve(int *first, int *last) {
    /* TODO: conditionally exchange the pointed-to endpoint values. */
    (void)first;
    (void)last;
}

static void print_array(const int *values, size_t length) {
    if (length == 0) { puts("EMPTY"); return; }
    for (size_t i = 0; i < length; i++) printf("%s%d", i == 0 ? "" : " ", values[i]);
    putchar('\n');
}

int main(int argc, char **argv) {
    size_t length = (size_t)(argc - 1);
    int *values = length == 0 ? NULL : malloc(length * sizeof *values);
    if (length != 0 && values == NULL) return 1;
    for (size_t i = 0; i < length; i++) values[i] = atoi(argv[i + 1]);
    if (length >= 2) solve(&values[0], &values[length - 1]);
    print_array(values, length);
    free(values);
    return 0;
}
