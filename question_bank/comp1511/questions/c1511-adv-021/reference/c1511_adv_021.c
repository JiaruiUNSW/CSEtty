#include <stdio.h>
#include <stdlib.h>

static size_t first_extreme_distance(const int *values, size_t length) {
    if (length < 2) return 0;
    size_t minimum = 0, maximum = 0;
    for (size_t i = 1; i < length; i++) {
        if (values[i] < values[minimum]) minimum = i;
        if (values[i] > values[maximum]) maximum = i;
    }
    return minimum > maximum ? minimum - maximum : maximum - minimum;
}

int main(int argc, char **argv) {
    size_t length = (size_t)(argc - 1);
    int *values = length == 0 ? NULL : malloc(length * sizeof *values);
    if (length != 0 && values == NULL) return 1;
    for (size_t i = 0; i < length; i++) values[i] = atoi(argv[i + 1]);
    printf("%zu\n", first_extreme_distance(values, length));
    free(values);
    return 0;
}
