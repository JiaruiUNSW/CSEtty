#include <stdio.h>
#define MAX_SIDE 20

static int row_range(const int grid[MAX_SIDE][MAX_SIDE], int row, int columns) {
    int minimum = grid[row][0];
    int maximum = grid[row][0];
    for (int column = 1; column < columns; column++) {
        if (grid[row][column] < minimum) minimum = grid[row][column];
        if (grid[row][column] > maximum) maximum = grid[row][column];
    }
    return maximum - minimum;
}

int main(void) {
    int rows, columns, tolerance;
    int grid[MAX_SIDE][MAX_SIDE];
    if (scanf("%d %d %d", &rows, &columns, &tolerance) != 3) return 1;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < columns; c++) scanf("%d", &grid[r][c]);
    int calm = 0;
    for (int r = 0; r < rows; r++)
        if (row_range(grid, r, columns) <= tolerance) calm++;
    printf("calm rows: %d\n", calm);
    return 0;
}

