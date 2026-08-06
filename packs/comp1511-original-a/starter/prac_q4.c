#include <stdio.h>
#define MAX 100
int count_peaks(int rows, int cols, int grid[MAX][MAX]) {
    // TODO: only interior cells have four neighbours.
    return 0;
}
int main(void) {
    int rows, cols, grid[MAX][MAX];
    scanf("%d %d", &rows, &cols);
    for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) scanf("%d", &grid[r][c]);
    printf("%d\n", count_peaks(rows, cols, grid));
    return 0;
}

