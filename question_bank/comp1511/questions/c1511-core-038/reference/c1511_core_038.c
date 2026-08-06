#include <stdio.h>
#define MAX_SIDE 20

static int flood(char grid[MAX_SIDE][MAX_SIDE + 1], int rows, int columns,
                 int row, int column) {
    if (row < 0 || row >= rows || column < 0 || column >= columns
        || grid[row][column] != '#')
        return 0;
    grid[row][column] = '.';
    return 1 + flood(grid, rows, columns, row - 1, column)
             + flood(grid, rows, columns, row + 1, column)
             + flood(grid, rows, columns, row, column - 1)
             + flood(grid, rows, columns, row, column + 1);
}

int main(void) {
    int rows, columns;
    char grid[MAX_SIDE][MAX_SIDE + 1];
    if (scanf("%d %d", &rows, &columns) != 2) return 1;
    for (int r = 0; r < rows; r++) scanf("%20s", grid[r]);
    int components = 0, largest = 0;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < columns; c++) {
            if (grid[r][c] == '#') {
                int size = flood(grid, rows, columns, r, c);
                components++;
                if (size > largest) largest = size;
            }
        }
    }
    printf("components: %d\nlargest: %d\n", components, largest);
    return 0;
}

