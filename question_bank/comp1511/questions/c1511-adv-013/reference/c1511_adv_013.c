#include <stdio.h>
#include <stdlib.h>

static void reverse(int *values, size_t left, size_t right) {
    while (left < right) {
        int temporary = values[left];
        values[left++] = values[right];
        values[right--] = temporary;
    }
}

static void solve(int *values, size_t length, size_t amount) {
    if (length == 0) return;
    amount %= length;
    if (amount == 0) return;
    reverse(values, 0, amount - 1);
    reverse(values, amount, length - 1);
    reverse(values, 0, length - 1);
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
