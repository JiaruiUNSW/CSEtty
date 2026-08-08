#include <stdio.h>

// TODO: repair the incorrect boundary logic in this function.
static int clamp(int lower, int upper, int value) {
    if (value < lower) {
        return upper;
    } else if (value > lower) {
        return lower;
    }
    return value;
}

int main(void) {
    int lower, upper, value;
    if (scanf("%d %d %d", &lower, &upper, &value) != 3)
        return 1;
    printf("clamped: %d\n", clamp(lower, upper, value));
    return 0;
}
