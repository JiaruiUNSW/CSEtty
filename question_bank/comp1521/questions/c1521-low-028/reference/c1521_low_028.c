#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

int main(void) {
    uint32_t bits;
    if (scanf("%" SCNx32, &bits) != 1) return 1;
    uint32_t exponent = (bits >> 23) & 0xffu;
    uint32_t fraction = bits & 0x7fffffu;
    const char *kind;
    if (exponent == 0) kind = fraction == 0 ? "zero" : "subnormal";
    else if (exponent == 0xffu) kind = fraction == 0 ? "infinity" : "nan";
    else kind = "normal";
    printf("%s\n", kind);
    return 0;
}
