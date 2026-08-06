#include <stdio.h>
#define MAX_VALUES 100

static int mismatch_count(const int a[], const int b[], int n, int shift) {
    int mismatches = 0;
    for (int i = 0; i < n; i++)
        if (a[(i + shift) % n] != b[i]) mismatches++;
    return mismatches;
}

int main(void) {
    int n, shift;
    int a[MAX_VALUES], b[MAX_VALUES];
    if (scanf("%d %d", &n, &shift) != 2) return 1;
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    for (int i = 0; i < n; i++) scanf("%d", &b[i]);
    printf("mismatches: %d\n", mismatch_count(a, b, n, shift));
    return 0;
}

