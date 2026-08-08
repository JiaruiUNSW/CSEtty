#include <stdio.h>

static long long solve(const int *values, int rows, int columns) {
    // TODO: Implement this function.
    (void)values;
    (void)rows;
    (void)columns;
    return 0;
}

int main(void) {
    int rows;
    int columns;
    int values[64];

    if (scanf("%d %d", &rows, &columns) != 2 || rows < 0 || columns < 0 || rows > 8 ||
        columns > 8) {
        return 1;
    }
    for (int i = 0; i < rows * columns; i++) {
        if (scanf("%d", &values[i]) != 1) {
            return 1;
        }
    }

    printf("result: %lld\n", solve(values, rows, columns));
    return 0;
}
