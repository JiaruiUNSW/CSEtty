#include <stdint.h>
#include <stdio.h>

static uint32_t solve(uint32_t x, uint32_t y, unsigned k) {
    // TODO: Implement this function.
    (void)x;
    (void)y;
    (void)k;
    return 0;
}

int main(void) {
    unsigned x;
    unsigned y;
    unsigned k;

    if (scanf("%x %x %u", &x, &y, &k) != 3) {
        return 1;
    }

    printf("result: %08x\n", solve(x, y, k));
    return 0;
}
