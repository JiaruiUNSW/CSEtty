#include <stdio.h>
#define MAX_WEIGHTS 100

static int count_balanced(const int weights[], int n) {
    int total = 0;
    for (int i = 0; i < n; i++) total += weights[i];
    int left = 0;
    int count = 0;
    for (int i = 0; i < n - 1; i++) {
        left += weights[i];
        if (left == total - left) count++;
    }
    return count;
}

int main(void) {
    int n;
    int weights[MAX_WEIGHTS];
    if (scanf("%d", &n) != 1) return 1;
    for (int i = 0; i < n; i++) scanf("%d", &weights[i]);
    printf("balanced cuts: %d\n", count_balanced(weights, n));
    return 0;
}

