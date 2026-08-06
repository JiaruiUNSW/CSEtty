#include <stdio.h>
#define MAX_READINGS 100

static int count_valleys(const int values[], int n) {
    int count = 0;
    for (int i = 1; i < n - 1; i++) {
        if (values[i] < values[i - 1] && values[i] < values[i + 1]) {
            count++;
        }
    }
    return count;
}

int main(void) {
    int n;
    int values[MAX_READINGS];
    if (scanf("%d", &n) != 1) return 1;
    for (int i = 0; i < n; i++) scanf("%d", &values[i]);
    printf("valleys: %d\n", count_valleys(values, n));
    return 0;
}

