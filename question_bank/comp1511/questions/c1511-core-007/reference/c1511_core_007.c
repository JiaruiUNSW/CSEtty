#include <stdio.h>
#define MAX_SIDE 20

static int is_warm(const int grid[MAX_SIDE][MAX_SIDE], int row, int column) {
    int neighbours = grid[row - 1][column] + grid[row + 1][column]
                   + grid[row][column - 1] + grid[row][column + 1];
    return 4 * grid[row][column] > neighbours;
}

int main(void) {
    int rows, columns;
    int grid[MAX_SIDE][MAX_SIDE];
    if (scanf("%d %d", &rows, &columns) != 2) return 1;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < columns; c++) scanf("%d", &grid[r][c]);
    int count = 0;
    for (int r = 1; r < rows - 1; r++)
        for (int c = 1; c < columns - 1; c++) count += is_warm(grid, r, c);
    printf("warm centres: %d\n", count);
    return 0;
}

