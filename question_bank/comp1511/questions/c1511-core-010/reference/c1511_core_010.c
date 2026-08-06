#include <stdio.h>
#define MAX_SIDE 20

static int diagonal_changes(const int grid[MAX_SIDE][MAX_SIDE], int n) {
    int changes = 0;
    for (int i = 1; i < n; i++)
        if (grid[i][i] != grid[i - 1][i - 1]) changes++;
    return changes;
}

int main(void) {
    int n;
    int grid[MAX_SIDE][MAX_SIDE];
    if (scanf("%d", &n) != 1) return 1;
    for (int r = 0; r < n; r++)
        for (int c = 0; c < n; c++) scanf("%d", &grid[r][c]);
    printf("diagonal changes: %d\n", diagonal_changes(grid, n));
    return 0;
}

