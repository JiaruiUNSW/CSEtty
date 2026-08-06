#include <stdio.h>
#include <string.h>

#define MAX_RECORDS 32
#define NAME_SIZE 21

struct record {
    char name[NAME_SIZE];
    int quantity;
};

int main(void) {
    /* TODO: implement the complete ADD, TAKE, SHOW, END interpreter. */
    char command[16];
    while (scanf("%15s", command) == 1) {
        if (strcmp(command, "END") == 0) break;
    }
    return 0;
}
