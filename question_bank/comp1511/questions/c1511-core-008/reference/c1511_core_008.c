#include <stdio.h>
#define MAX_SIDE 20

static int frame_checksum(const int grid[MAX_SIDE][MAX_SIDE], int rows, int columns) {
    int checksum = 0;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < columns; c++) {
            int border = r == 0 || r == rows - 1 || c == 0 || c == columns - 1;
            if (border) checksum += grid[r][c];
            else checksum -= grid[r][c];
        }
    }
    return checksum;
}

int main(void) {
    int rows, columns;
    int grid[MAX_SIDE][MAX_SIDE];
    if (scanf("%d %d", &rows, &columns) != 2) return 1;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < columns; c++) scanf("%d", &grid[r][c]);
    printf("checksum: %d\n", frame_checksum(grid, rows, columns));
    return 0;
}

