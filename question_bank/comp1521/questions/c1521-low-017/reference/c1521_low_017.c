#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

int main(void) {
    uint32_t value;
    unsigned index;
    if (scanf("%" SCNx32 " %u", &value, &index) != 2) return 1;
    uint32_t byte = (value >> (8u * index)) & UINT32_C(0xff);
    printf("%" PRIu32 "\n", byte);
    return 0;
}
