#include <stdint.h>
#include <stdio.h>

static long long solve(uint32_t cp) {
    // TODO: Implement this function.
    (void)cp;
    return 0;
}

int main(void) {
    unsigned cp;

    if (scanf("%x", &cp) != 1) {
        return 1;
    }

    printf("result: %lld\n", solve(cp));
    return 0;
}
