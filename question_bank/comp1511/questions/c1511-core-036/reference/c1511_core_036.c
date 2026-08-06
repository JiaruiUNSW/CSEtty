#include <stdio.h>
#define MAX_LINE 1000

static int is_digit(char ch) {
    return ch >= '0' && ch <= '9';
}

int main(void) {
    char line[MAX_LINE + 2];
    if (fgets(line, sizeof line, stdin) == NULL) return 1;
    int in_digits = 0, redactions = 0;
    for (int i = 0; line[i] != '\0' && line[i] != '\n'; i++) {
        if (is_digit(line[i])) {
            if (!in_digits) {
                putchar('#');
                redactions++;
                in_digits = 1;
            }
        } else {
            putchar(line[i]);
            in_digits = 0;
        }
    }
    printf("\nredactions: %d\n", redactions);
    return 0;
}

