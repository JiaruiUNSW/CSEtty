#include <stdio.h>
#define MAX_ITEMS 100

struct item {
    int id;
    int current;
    int target;
};

static int needed(struct item item) {
    if (item.current < item.target) return item.target - item.current;
    return 0;
}

int main(void) {
    int n;
    struct item items[MAX_ITEMS];
    if (scanf("%d", &n) != 1) return 1;
    for (int i = 0; i < n; i++)
        scanf("%d %d %d", &items[i].id, &items[i].current, &items[i].target);
    int total = 0;
    for (int i = 0; i < n; i++) {
        int amount = needed(items[i]);
        if (amount > 0) printf("%d: %d\n", items[i].id, amount);
        total += amount;
    }
    printf("total needed: %d\n", total);
    return 0;
}

