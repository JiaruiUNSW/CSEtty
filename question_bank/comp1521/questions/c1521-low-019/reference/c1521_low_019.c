#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

int main(void) {
    uint32_t value;
    unsigned k;
    if (scanf("%" SCNx32 " %u", &value, &k) != 2) return 1;
    uint32_t result = k == 0 ? value : (value << k) | (value >> (32u - k));
    printf("%08" PRIx32 "\n", result);
    return 0;
}
