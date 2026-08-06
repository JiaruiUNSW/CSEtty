#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

int main(void) {
    uint32_t opcode, rs, rt;
    int32_t immediate;
    if (scanf("%" SCNu32 " %" SCNu32 " %" SCNu32 " %" SCNd32,
              &opcode, &rs, &rt, &immediate) != 4) return 1;
    uint32_t word = ((opcode & 0x3fu) << 26)
                  | ((rs & 0x1fu) << 21)
                  | ((rt & 0x1fu) << 16)
                  | (uint16_t)immediate;
    printf("%08" PRIx32 "\n", word);
    return 0;
}
