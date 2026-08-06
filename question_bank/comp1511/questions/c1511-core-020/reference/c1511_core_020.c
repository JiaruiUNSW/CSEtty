#include <stdio.h>

int main(void) {
    int start, end;
    if (scanf("%d %d", &start, &end) != 2) return 1;
    int change = end - start;
    const char *direction = "steady";
    if (change > 0) direction = "rising";
    else if (change < 0) direction = "falling";
    printf("change: %d\ndirection: %s\n", change, direction);
    return 0;
}

