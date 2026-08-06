#include <stdio.h>
#include <stdlib.h>

static void solve(int *values, size_t length, size_t amount) {
    /* TODO: rotate the supplied array in place. */
    (void)values;
    (void)length;
    (void)amount;
}

static void print_array(const int *values, size_t length) {
    if (length == 0) {
        puts("EMPTY");
        return;
    }
    for (size_t i = 0; i < length; i++) printf("%s%d", i == 0 ? "" : " ", values[i]);
    putchar('\n');
}

int main(int argc, char **argv) {
    if (argc < 2) return 2;
    size_t length = (size_t)(argc - 2);
    int *values = length == 0 ? NULL : malloc(length * sizeof *values);
    if (length != 0 && values == NULL) return 1;
    for (size_t i = 0; i < length; i++) values[i] = atoi(argv[i + 2]);
    solve(values, length, (size_t)strtoul(argv[1], NULL, 10));
    print_array(values, length);
    free(values);
    return 0;
}
