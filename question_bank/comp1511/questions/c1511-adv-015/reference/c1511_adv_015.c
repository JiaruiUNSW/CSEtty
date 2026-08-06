#include <stdio.h>
#include <stdlib.h>

static int *solve(const int *values, size_t length, int low, int high, size_t *result_length) {
    size_t count = 0;
    for (size_t i = 0; i < length; i++) {
        if (values[i] >= low && values[i] <= high) count++;
    }
    *result_length = count;
    if (count == 0) return NULL;
    int *result = malloc(count * sizeof *result);
    if (result == NULL) exit(1);
    size_t write = 0;
    for (size_t i = 0; i < length; i++) {
        if (values[i] >= low && values[i] <= high) result[write++] = values[i];
    }
    return result;
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
    if (argc < 3) return 2;
    size_t length = (size_t)(argc - 3);
    int *values = length == 0 ? NULL : malloc(length * sizeof *values);
    if (length != 0 && values == NULL) return 1;
    for (size_t i = 0; i < length; i++) values[i] = atoi(argv[i + 3]);
    size_t result_length = 0;
    int *result = solve(values, length, atoi(argv[1]), atoi(argv[2]), &result_length);
    print_array(result, result_length);
    free(result);
    free(values);
    return 0;
}
