#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct buffer {
    int *data;
    size_t length;
    size_t capacity;
};

int main(void) {
    struct buffer buffer = {NULL, 0, 0};
    // TODO: implement PUSH, DROP, ROLL, UNIQUE, PRINT, and END.
    char command[16];
    while (scanf("%15s", command) == 1) {
        if (strcmp(command, "END") == 0)
            break;
    }
    free(buffer.data);
    return 0;
}
