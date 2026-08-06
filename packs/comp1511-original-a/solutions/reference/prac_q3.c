#include <stdio.h>
#include <stdlib.h>
struct node { int data; struct node *next; };
struct node *delete_first_negative(struct node *head) {
    struct node **link = &head;
    while (*link != NULL && (*link)->data >= 0) link = &(*link)->next;
    if (*link != NULL) { struct node *removed = *link; *link = removed->next; free(removed); }
    return head;
}
int main(int argc, char **argv) {
    struct node *head = NULL, **tail = &head;
    for (int i = 1; i < argc; i++) { *tail = malloc(sizeof **tail); (*tail)->data = atoi(argv[i]); (*tail)->next = NULL; tail = &(*tail)->next; }
    head = delete_first_negative(head);
    for (struct node *p = head; p != NULL; p = p->next) printf("%d%s", p->data, p->next == NULL ? "\n" : " ");
    if (head == NULL) printf("empty\n");
    while (head != NULL) { struct node *next = head->next; free(head); head = next; }
    return 0;
}

