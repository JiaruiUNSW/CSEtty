#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
uint32_t rotate_right(uint32_t value, unsigned amount) {
    // TODO: amount is between 0 and 31 inclusive.
    return value;
}
int main(int argc, char **argv) { if (argc == 3) printf("%u\n", rotate_right((uint32_t)strtoul(argv[1], NULL, 0), (unsigned)strtoul(argv[2], NULL, 0))); return 0; }

