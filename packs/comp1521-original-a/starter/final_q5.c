#include <stdio.h>

int main(void) {
    int codepoints = 0;
    int byte;
    while ((byte = getchar()) != EOF) {
        // TODO: continuation bytes have binary prefix 10.
    }
    printf("%d\n", codepoints);
    return 0;
}
