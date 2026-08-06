#include <stdio.h>
#define MAX_SIZE 100
int border_sum(int size, int grid[MAX_SIZE][MAX_SIZE]) {
    int sum = 0;
    for (int row = 0; row < size; row++) {
        for (int col = 0; col < size; col++) {
            if (row == 0 || row == size - 1 || col == 0 || col == size - 1) sum += grid[row][col];
        }
    }
    return sum;
}
int main(void) {
    int size, grid[MAX_SIZE][MAX_SIZE];
    scanf("%d", &size);
    for (int r = 0; r < size; r++) for (int c = 0; c < size; c++) scanf("%d", &grid[r][c]);
    printf("%d\n", border_sum(size, grid));
    return 0;
}

