#include <stdio.h>
#define MAX 100
int count_peaks(int rows, int cols, int grid[MAX][MAX]) {
    int count = 0;
    for (int r = 1; r + 1 < rows; r++) for (int c = 1; c + 1 < cols; c++) {
        int x = grid[r][c];
        if (x > grid[r - 1][c] && x > grid[r + 1][c] && x > grid[r][c - 1] && x > grid[r][c + 1]) count++;
    }
    return count;
}
int main(void) {
    int rows, cols, grid[MAX][MAX]; scanf("%d %d", &rows, &cols);
    for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) scanf("%d", &grid[r][c]);
    printf("%d\n", count_peaks(rows, cols, grid)); return 0;
}

