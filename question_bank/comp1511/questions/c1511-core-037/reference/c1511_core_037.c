#include <stdio.h>
#define MAX_VALUES 100

static int window_range(const int values[], int start, int width) {
    int minimum = values[start], maximum = values[start];
    for (int i = start + 1; i < start + width; i++) {
        if (values[i] < minimum) minimum = values[i];
        if (values[i] > maximum) maximum = values[i];
    }
    return maximum - minimum;
}

int main(void) {
    int n, width, threshold;
    int values[MAX_VALUES];
    if (scanf("%d %d %d", &n, &width, &threshold) != 3) return 1;
    for (int i = 0; i < n; i++) scanf("%d", &values[i]);
    int anomalies = 0;
    int maximum = window_range(values, 0, width);
    for (int start = 0; start <= n - width; start++) {
        int range = window_range(values, start, width);
        if (range >= threshold) anomalies++;
        if (range > maximum) maximum = range;
    }
    printf("anomalies: %d\nmaximum range: %d\n", anomalies, maximum);
    return 0;
}

