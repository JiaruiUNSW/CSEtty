#include <stdio.h>

struct time {
    int hour;
    int minute;
};

static int minutes_after_midnight(struct time value) {
    return value.hour * 60 + value.minute;
}

int main(void) {
    struct time start, end;
    if (scanf("%d %d %d %d", &start.hour, &start.minute, &end.hour, &end.minute) != 4)
        return 1;
    printf("elapsed: %d minutes\n",
           minutes_after_midnight(end) - minutes_after_midnight(start));
    return 0;
}

