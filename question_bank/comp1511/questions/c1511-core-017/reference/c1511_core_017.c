#include <stdio.h>

int main(void) {
    int depth = 0, maximum = 0, valid = 1;
    int ch;
    while ((ch = getchar()) != EOF && ch != '\n') {
        if (ch == '(') {
            depth++;
            if (depth > maximum) maximum = depth;
        } else if (ch == ')') {
            if (depth == 0) valid = 0;
            else depth--;
        }
    }
    if (depth != 0) valid = 0;
    printf("valid: %s\nmax depth: %d\n", valid ? "yes" : "no", maximum);
    return 0;
}

