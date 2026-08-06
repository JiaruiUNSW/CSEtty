#include <stdio.h>

int main(void) {
    int ch;
    int wrote = 0;
    int pending_space = 0;
    while ((ch = getchar()) != EOF && ch != '\n') {
        if (ch == ' ' || ch == '\t') {
            if (wrote) pending_space = 1;
        } else {
            if (pending_space) putchar(' ');
            putchar(ch);
            wrote = 1;
            pending_space = 0;
        }
    }
    putchar('\n');
    return 0;
}

