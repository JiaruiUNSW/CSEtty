#include <stdio.h>
#include <stdlib.h>

static size_t first_extreme_distance(const int *values, size_t length) {
    // TODO: return the distance between first extrema.
    (void)values;
    (void)length;
    return 0;
}

int main(int argc, char **argv) {
    size_t length = (size_t)(argc - 1);
    int *values = length == 0 ? NULL : malloc(length * sizeof *values);
    if (length != 0 && values == NULL)
        return 1;
    for (size_t i = 0; i < length; i++)
        values[i] = atoi(argv[i + 1]);
    printf("%zu\n", first_extreme_distance(values, length));
    free(values);
    return 0;
}
