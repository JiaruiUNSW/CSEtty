#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

int main(void) {
    uint32_t word;
    if (scanf("%" SCNx32, &word) != 1) return 1;
    uint32_t rs = (word >> 21) & 0x1fu;
    uint32_t rt = (word >> 16) & 0x1fu;
    uint32_t rd = (word >> 11) & 0x1fu;
    uint32_t shamt = (word >> 6) & 0x1fu;
    uint32_t funct = word & 0x3fu;
    printf("%" PRIu32 " %" PRIu32 " %" PRIu32 " %" PRIu32 " %" PRIu32 "\n",
           rs, rt, rd, shamt, funct);
    return 0;
}
