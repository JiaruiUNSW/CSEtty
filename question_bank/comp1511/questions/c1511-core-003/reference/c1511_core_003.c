#include <stdio.h>
#define MAX_POINTS 100

static int absolute(int value) {
    return value < 0 ? -value : value;
}

static int cyclic_distance(const int labels[], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        int next = (i + 1) % n;
        sum += absolute(labels[next] - labels[i]);
    }
    return sum;
}

int main(void) {
    int n;
    int labels[MAX_POINTS];
    if (scanf("%d", &n) != 1) return 1;
    for (int i = 0; i < n; i++) scanf("%d", &labels[i]);
    printf("distance: %d\n", cyclic_distance(labels, n));
    return 0;
}

