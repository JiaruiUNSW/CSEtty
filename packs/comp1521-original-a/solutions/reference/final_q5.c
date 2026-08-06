#include <stdio.h>

int main(void) {
    int count = 0;
    int byte;
    while ((byte = getchar()) != EOF) {
        if (((unsigned)byte & 0xC0u) != 0x80u) {
            count++;
        }
    }
    printf("%d\n", count);
    return 0;
}
