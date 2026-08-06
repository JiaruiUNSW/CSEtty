#include <stdio.h>
#include <stdlib.h>

struct node { int data; struct node *next; };

int count_sign_changes(struct node *head) {
    int count = 0;
    for (struct node *p = head; p != NULL && p->next != NULL; p = p->next) {
        int a = p->data;
        int b = p->next->data;
        if (a != 0 && b != 0 && ((a < 0 && b > 0) || (a > 0 && b < 0))) count++;
    }
    return count;
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
    while (head != NULL) { struct node *next = head->next; free(head); head = next; }
    return 0;
}

