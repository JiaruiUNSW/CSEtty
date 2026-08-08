#include <stdio.h>

static long long solve(int a, int b, int c) {
    // TODO: Implement this function.
    (void)a;
    (void)b;
    (void)c;
    return 0;
}

int main(void) {
    int a;
    int b;
    int c;

    if (scanf("%d %d %d", &a, &b, &c) != 3) {
        return 1;
    }

    printf("result: %lld\n", solve(a, b, c));
    return 0;
}
