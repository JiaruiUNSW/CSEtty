#include <stdio.h>

static int letter_value(int ch) {
    if (ch >= 'A' && ch <= 'Z') return ch - 'A' + 1;
    if (ch >= 'a' && ch <= 'z') return ch - 'a' + 1;
    return 0;
}

int main(void) {
    int ch, position = 0, checksum = 0;
    while ((ch = getchar()) != EOF && ch != '\n') {
        int value = letter_value(ch);
        if (value != 0) {
            position++;
            checksum += position * value;
        }
    }
    printf("checksum: %d\n", checksum);
    return 0;
}

