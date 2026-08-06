#include <stdio.h>

int main(void) {
    int value;
    if (scanf("%d", &value) != 1) return 1;
    int score = 0;
    int sign = 1;
    do {
        score += sign * (value % 10);
        sign = -sign;
        value /= 10;
    } while (value > 0);
    printf("score: %d\n", score);
    return 0;
}

