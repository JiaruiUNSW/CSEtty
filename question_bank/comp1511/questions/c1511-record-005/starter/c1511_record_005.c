#include <stdio.h>

struct record {
    char name[32];
    int value;
};

static long long solve(const struct record *records, int n) {
    // TODO: Implement this function.
    (void)records;
    (void)n;
    return 0;
}

int main(void) {
    int n;
    struct record records[50];

    if (scanf("%d", &n) != 1 || n < 0 || n > 50) {
        return 1;
    }
    for (int i = 0; i < n; i++) {
        if (scanf("%31s %d", records[i].name, &records[i].value) != 2) {
            return 1;
        }
    }

    printf("result: %lld\n", solve(records, n));
    return 0;
}
