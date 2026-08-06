#include <stdio.h>
#define MAX_SIDE 20

static int has_unique_maximum(const int grid[MAX_SIDE][MAX_SIDE], int rows, int column) {
    int maximum = grid[0][column];
    int occurrences = 1;
    for (int row = 1; row < rows; row++) {
        if (grid[row][column] > maximum) {
            maximum = grid[row][column];
            occurrences = 1;
        } else if (grid[row][column] == maximum) {
            occurrences++;
        }
    }
    return occurrences == 1;
}

int main(void) {
    int rows, columns;
    int grid[MAX_SIDE][MAX_SIDE];
    if (scanf("%d %d", &rows, &columns) != 2) return 1;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < columns; c++) scanf("%d", &grid[r][c]);
    int count = 0;
    for (int c = 0; c < columns; c++) count += has_unique_maximum(grid, rows, c);
    printf("unique beacons: %d\n", count);
    return 0;
}

