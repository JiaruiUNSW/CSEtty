#include <stdio.h>

#define MAX_SIZE 100

int border_sum(int size, int grid[MAX_SIZE][MAX_SIZE]) {
    // TODO: sum each border cell exactly once.
    return 0;
}

int main(void) {
    int size;
    int grid[MAX_SIZE][MAX_SIZE];
    scanf("%d", &size);
    for (int row = 0; row < size; row++)
        for (int col = 0; col < size; col++) scanf("%d", &grid[row][col]);
    printf("%d\n", border_sum(size, grid));
    return 0;
}

