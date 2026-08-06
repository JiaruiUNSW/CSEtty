#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NAME_SIZE 21

struct node {
    char name[NAME_SIZE];
    struct node *next;
};

/* TODO: add helper functions and implement all commands safely. */
int main(void) {
    struct node *head = NULL;
    char command[16];
    while (scanf("%15s", command) == 1) {
        if (strcmp(command, "END") == 0) break;
    }
    free(head);
    return 0;
}
