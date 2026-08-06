#include <stdio.h>
#define MAX_SIDE 20

static void row_stats(const int grid[MAX_SIDE][MAX_SIDE], int row, int columns,
                      int *sum, int *range) {
    int total = grid[row][0];
    int minimum = grid[row][0], maximum = grid[row][0];
    for (int c = 1; c < columns; c++) {
        total += grid[row][c];
        if (grid[row][c] < minimum) minimum = grid[row][c];
        if (grid[row][c] > maximum) maximum = grid[row][c];
    }
    *sum = total;
    *range = maximum - minimum;
}

int main(void) {
    int rows, columns;
    int grid[MAX_SIDE][MAX_SIDE];
    if (scanf("%d %d", &rows, &columns) != 2) return 1;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < columns; c++) scanf("%d", &grid[r][c]);
    int best_row = 0, best_sum, best_range;
    row_stats(grid, 0, columns, &best_sum, &best_range);
    for (int r = 1; r < rows; r++) {
        int sum, range;
        row_stats(grid, r, columns, &sum, &range);
        if (sum > best_sum || (sum == best_sum && range < best_range)) {
            best_row = r;
            best_sum = sum;
            best_range = range;
        }
    }
    printf("row: %d\nsum: %d\nrange: %d\n", best_row, best_sum, best_range);
    return 0;
}

