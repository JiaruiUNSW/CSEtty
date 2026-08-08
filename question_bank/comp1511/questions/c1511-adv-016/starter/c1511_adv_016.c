#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int *merge_unique(const int *left, size_t left_length, const int *right,
                         size_t right_length, size_t *result_length) {
    // TODO: return a newly allocated sorted union.
    (void)left;
    (void)left_length;
    (void)right;
    (void)right_length;
    *result_length = 0;
    return NULL;
}

static void print_array(const int *values, size_t length) {
    if (length == 0) {
        puts("EMPTY");
        return;
    }
    for (size_t i = 0; i < length; i++)
        printf("%s%d", i == 0 ? "" : " ", values[i]);
    putchar('\n');
}

int main(int argc, char **argv) {
    int divider = -1;
    for (int i = 1; i < argc; i++)
        if (strcmp(argv[i], "--") == 0)
            divider = i;
    if (divider < 0)
        return 2;
    size_t left_length = (size_t)(divider - 1);
    size_t right_length = (size_t)(argc - divider - 1);
    int *left = left_length == 0 ? NULL : malloc(left_length * sizeof *left);
    int *right = right_length == 0 ? NULL : malloc(right_length * sizeof *right);
    if ((left_length != 0 && left == NULL) || (right_length != 0 && right == NULL))
        return 1;
    for (size_t i = 0; i < left_length; i++)
        left[i] = atoi(argv[i + 1]);
    for (size_t i = 0; i < right_length; i++)
        right[i] = atoi(argv[divider + 1 + (int)i]);
    size_t result_length = 0;
    int *result = merge_unique(left, left_length, right, right_length, &result_length);
    print_array(result, result_length);
    free(result);
    free(left);
    free(right);
    return 0;
}
