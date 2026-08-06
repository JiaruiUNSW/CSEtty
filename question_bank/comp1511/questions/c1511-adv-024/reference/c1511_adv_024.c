#include <stdio.h>
#include <stdlib.h>

static int solve(int **values, size_t *length) {
    int checksum = 0;
    for (size_t i = 0; i < *length; i++) checksum += (*values)[i];
    int *grown = realloc(*values, (*length + 1) * sizeof *grown);
    if (grown == NULL) return 0;
    grown[*length] = checksum;
    *values = grown;
    (*length)++;
    return 1;
}

static void print_array(const int *values, size_t length) {
    for (size_t i = 0; i < length; i++) printf("%s%d", i == 0 ? "" : " ", values[i]);
    putchar('\n');
}

int main(int argc, char **argv) {
    size_t length = (size_t)(argc - 1);
    int *values = length == 0 ? NULL : malloc(length * sizeof *values);
    if (length != 0 && values == NULL) return 1;
    for (size_t i = 0; i < length; i++) values[i] = atoi(argv[i + 1]);
    if (!solve(&values, &length)) { free(values); return 1; }
    print_array(values, length);
    free(values);
    return 0;
}
