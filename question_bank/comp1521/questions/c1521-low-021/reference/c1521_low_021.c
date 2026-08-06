#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

int main(void) {
    uint16_t x, y;
    if (scanf("%" SCNx16 " %" SCNx16, &x, &y) != 2) return 1;
    uint32_t result = 0;
    for (unsigned i = 0; i < 16; i++) {
        result |= ((uint32_t)(x >> i) & 1u) << (2u * i);
        result |= ((uint32_t)(y >> i) & 1u) << (2u * i + 1u);
    }
    printf("%08" PRIx32 "\n", result);
    return 0;
}
