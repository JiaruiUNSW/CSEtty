#include <stdio.h>
#include <string.h>

#define MAX_CATEGORIES 32
#define MAX_HISTORY 100
#define NAME_SIZE 21

struct counter {
    char name[NAME_SIZE];
    int count;
};

int main(void) {
    /* TODO: implement LOG, UNDO, COUNT, TOTAL, and END. */
    char command[16];
    while (scanf("%15s", command) == 1) {
        if (strcmp(command, "END") == 0) break;
    }
    return 0;
}
