#include <stdio.h>

struct parcel {
    int weight;
    int length;
    int width;
    int height;
};

static const char *classify(struct parcel item) {
    int volume = item.length * item.width * item.height;
    if (item.length > 50 || item.width > 50 || item.height > 50 || volume > 50000)
        return "oversized";
    if (item.weight <= 5 && volume <= 1000) return "compact";
    return "standard";
}

int main(void) {
    struct parcel item;
    if (scanf("%d %d %d %d", &item.weight, &item.length, &item.width, &item.height) != 4)
        return 1;
    printf("class: %s\n", classify(item));
    return 0;
}

