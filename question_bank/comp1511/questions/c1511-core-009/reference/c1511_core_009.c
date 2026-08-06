#include <stdio.h>
#define MAX_SIDE 20

static int is_rising(const int grid[MAX_SIDE][MAX_SIDE], int rows, int column) {
    for (int r = 1; r < rows; r++)
        if (grid[r][column] <= grid[r - 1][column]) return 0;
    return 1;
}

int main(void) {
    int rows, columns;
    int grid[MAX_SIDE][MAX_SIDE];
    if (scanf("%d %d", &rows, &columns) != 2) return 1;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < columns; c++) scanf("%d", &grid[r][c]);
    int count = 0;
    for (int c = 0; c < columns; c++) count += is_rising(grid, rows, c);
    printf("rising columns: %d\n", count);
    return 0;
}

