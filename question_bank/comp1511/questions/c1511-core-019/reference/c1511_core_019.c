#include <stdio.h>

static int clamp(int lower, int upper, int value) {
    if (value < lower) return lower;
    if (value > upper) return upper;
    return value;
}

int main(void) {
    int lower, upper, value;
    if (scanf("%d %d %d", &lower, &upper, &value) != 3) return 1;
    printf("clamped: %d\n", clamp(lower, upper, value));
    return 0;
}

