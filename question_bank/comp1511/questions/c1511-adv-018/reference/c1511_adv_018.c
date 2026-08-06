#include <stdio.h>
#include <stdlib.h>

static size_t solve(int *values, size_t length, int low, int high) {
    size_t changed = 0;
    for (size_t i = 0; i < length; i++) {
        if (values[i] < low) {
            values[i] = low;
            changed++;
        } else if (values[i] > high) {
            values[i] = high;
            changed++;
        }
    }
    return changed;
}

static void print_array(const int *values, size_t length) {
    if (length == 0) { puts("EMPTY"); return; }
    for (size_t i = 0; i < length; i++) printf("%s%d", i == 0 ? "" : " ", values[i]);
    putchar('\n');
}

int main(int argc, char **argv) {
    if (argc < 3) return 2;
    size_t length = (size_t)(argc - 3);
    int *values = length == 0 ? NULL : malloc(length * sizeof *values);
    if (length != 0 && values == NULL) return 1;
    for (size_t i = 0; i < length; i++) values[i] = atoi(argv[i + 3]);
    printf("changes=%zu\n", solve(values, length, atoi(argv[1]), atoi(argv[2])));
    print_array(values, length);
    free(values);
    return 0;
}
