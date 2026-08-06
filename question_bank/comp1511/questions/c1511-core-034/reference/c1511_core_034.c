#include <stdio.h>
#define MAX_SIDE 20

static int window_sum(const int grid[MAX_SIDE][MAX_SIDE], int row, int column) {
    return grid[row][column] + grid[row][column + 1]
         + grid[row + 1][column] + grid[row + 1][column + 1];
}

int main(void) {
    int rows, columns;
    int grid[MAX_SIDE][MAX_SIDE];
    if (scanf("%d %d", &rows, &columns) != 2) return 1;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < columns; c++) scanf("%d", &grid[r][c]);
    int best_row = 0, best_column = 0;
    int best_sum = window_sum(grid, 0, 0);
    for (int r = 0; r < rows - 1; r++) {
        for (int c = 0; c < columns - 1; c++) {
            int sum = window_sum(grid, r, c);
            if (sum > best_sum) {
                best_sum = sum;
                best_row = r;
                best_column = c;
            }
        }
    }
    printf("top: %d %d\nsum: %d\n", best_row, best_column, best_sum);
    return 0;
}

