#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

int main(void) {
    uint32_t value, set_mask, clear_mask;
    if (scanf("%" SCNx32 " %" SCNx32 " %" SCNx32,
              &value, &set_mask, &clear_mask) != 3) return 1;
    uint32_t result = (value | set_mask) & ~clear_mask;
    printf("%08" PRIx32 "\n", result);
    return 0;
}
