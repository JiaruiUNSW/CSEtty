#include <stdio.h>
#include <stdlib.h>

struct node { int data; struct node *next; };

struct node *delete_first_negative(struct node *head) {
    // TODO: unlink and free the first negative node.
    return head;
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
    head = delete_first_negative(head);
    for (struct node *p = head; p != NULL; p = p->next)
        printf("%d%s", p->data, p->next == NULL ? "\n" : " ");
    if (head == NULL) printf("empty\n");
    while (head != NULL) { struct node *next = head->next; free(head); head = next; }
    return 0;
}

