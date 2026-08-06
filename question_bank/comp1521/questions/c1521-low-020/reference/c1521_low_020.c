#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

int main(void) {
    uint32_t raw;
    if (scanf("%" SCNx32, &raw) != 1) return 1;
    raw &= UINT32_C(0xfff);
    if ((raw & UINT32_C(0x800)) != 0) raw |= UINT32_C(0xfffff000);
    printf("%" PRId32 "\n", (int32_t)raw);
    return 0;
}
