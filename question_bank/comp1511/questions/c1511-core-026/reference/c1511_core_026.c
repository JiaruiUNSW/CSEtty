#include <stdio.h>

int main(void) {
    int hour, minute, offset;
    if (scanf("%d %d %d", &hour, &minute, &offset) != 3) return 1;
    int total = (hour * 60 + minute + offset) % 1440;
    if (total < 0) total += 1440;
    printf("%02d:%02d\n", total / 60, total % 60);
    return 0;
}

