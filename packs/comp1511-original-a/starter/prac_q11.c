#include <stdio.h>
#include <string.h>
int main(void) {
    int accumulator = 0;
    char command[16];
    while (scanf("%15s", command) == 1) {
        if (strcmp(command, "quit") == 0) break;
        // TODO: implement add, mul, and print.
    }
    (void)accumulator;
    return 0;
}

