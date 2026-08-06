#include <stdio.h>
#include <stdlib.h>

struct node {
    int data;
    struct node *next;
};

int count_sign_changes(struct node *head) {
    // TODO: count adjacent, non-zero values with different signs.
    return 0;
}

int main(int argc, char **argv) {
    struct node *head = NULL;
    struct node **tail = &head;
    for (int i = 1; i < argc; i++) {
        *tail = malloc(sizeof **tail);
        (*tail)->data = atoi(argv[i]);
        (*tail)->next = NULL;
        tail = &(*tail)->next;
    }
    printf("%d\n", count_sign_changes(head));
    while (head != NULL) {
        struct node *next = head->next;
        free(head);
        head = next;
    }
    return 0;
}

