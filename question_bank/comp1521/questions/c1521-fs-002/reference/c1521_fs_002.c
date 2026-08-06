#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int fail(void) { fputs("c1521_fs_002: error\n", stderr); return 1; }

int main(int argc, char **argv) {
    if (argc != 2) return fail();
    FILE *out = fopen(argv[1], "wb");
    if (out == NULL) return fail();
    char line[256];
    while (fgets(line, sizeof line, stdin) != NULL) {
        char *end = NULL;
        errno = 0;
        unsigned long long raw = strtoull(line, &end, 10);
        if (errno != 0 || end == line || (*end != '\n' && *end != '\0') || raw > UINT32_MAX) { fclose(out); return fail(); }
        uint32_t value = (uint32_t)raw;
        unsigned char b[4] = {(unsigned char)(value >> 24), (unsigned char)(value >> 16), (unsigned char)(value >> 8), (unsigned char)value};
        if (fwrite(b, 1, 4, out) != 4) { fclose(out); return fail(); }
    }
    if (ferror(stdin) || fclose(out) != 0) return fail();
    FILE *in = fopen(argv[1], "rb");
    if (in == NULL) return fail();
    uint64_t count = 0;
    uint32_t checksum = 0;
    unsigned char b[4];
    size_t got;
    while ((got = fread(b, 1, 4, in)) == 4) {
        uint32_t value = ((uint32_t)b[0] << 24) | ((uint32_t)b[1] << 16) | ((uint32_t)b[2] << 8) | b[3];
        checksum += value;
        count++;
    }
    if (got != 0 || ferror(in) || fclose(in) != 0) return fail();
    printf("count=%llu checksum=%u\n", (unsigned long long)count, checksum);
    return 0;
}
