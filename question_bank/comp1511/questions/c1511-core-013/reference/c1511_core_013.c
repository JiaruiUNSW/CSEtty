#include <stdio.h>

int main(void) {
    int distance, peak;
    if (scanf("%d %d", &distance, &peak) != 2) return 1;
    int fare = 4;
    if (distance > 15) fare += 7;
    else if (distance > 5) fare += 3;
    if (peak == 1) fare += 2;
    printf("fare: $%d\n", fare);
    return 0;
}

