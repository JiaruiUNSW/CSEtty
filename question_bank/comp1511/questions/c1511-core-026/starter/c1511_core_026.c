#include <stdio.h>

int main(void) {
    int hour, minute, offset;
    if (scanf("%d %d %d", &hour, &minute, &offset) != 3) return 1;

    // TODO: repair the wrap unit and negative-offset handling.
    int total = hour * 60 + minute + offset;
    total %= 24;

    printf("%02d:%02d\n", total / 60, total % 60);
    return 0;
}

