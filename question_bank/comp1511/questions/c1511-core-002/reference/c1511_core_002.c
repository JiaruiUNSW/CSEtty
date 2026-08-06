#include <stdio.h>
#define MAX_VALUES 100

static int longest_climb(const int values[], int n) {
    int current = 1;
    int best = 1;
    for (int i = 1; i < n; i++) {
        if (values[i] >= values[i - 1]) current++;
        else current = 1;
        if (current > best) best = current;
    }
    return best;
}

int main(void) {
    int n;
    int values[MAX_VALUES];
    if (scanf("%d", &n) != 1) return 1;
    for (int i = 0; i < n; i++) scanf("%d", &values[i]);
    printf("longest: %d\n", longest_climb(values, n));
    return 0;
}

