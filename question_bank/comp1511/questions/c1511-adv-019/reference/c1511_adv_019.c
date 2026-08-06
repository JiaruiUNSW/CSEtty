#include <stdio.h>
#include <stdlib.h>

static void solve(int *values, size_t length) {
    if (length == 0) return;
    int previous = values[0];
    for (size_t i = 1; i < length; i++) {
        int current = values[i];
        values[i] = current - previous;
        previous = current;
    }
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
    solve(values, length);
    print_array(values, length);
    free(values);
    return 0;
}
