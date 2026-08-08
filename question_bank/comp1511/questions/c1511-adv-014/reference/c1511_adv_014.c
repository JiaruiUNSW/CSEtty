#include <stdio.h>
#include <stdlib.h>

static size_t compact_runs(int *values, size_t length) {
    if (length == 0) return 0;
    size_t write = 1;
    for (size_t read = 1; read < length; read++) {
        if (values[read] != values[write - 1]) values[write++] = values[read];
    }
    return write;
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
    size_t length = (size_t)(argc - 1);
    int *values = length == 0 ? NULL : malloc(length * sizeof *values);
    if (length != 0 && values == NULL) return 1;
    for (size_t i = 0; i < length; i++) values[i] = atoi(argv[i + 1]);
    size_t kept = compact_runs(values, length);
    print_array(values, kept);
    free(values);
    return 0;
}
