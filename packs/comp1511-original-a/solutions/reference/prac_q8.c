#include <stdio.h>
#include <stdlib.h>
struct node { char value; struct node *next; };
int count_digits(struct node *head) { int count = 0; for (; head != NULL; head = head->next) if (head->value >= '0' && head->value <= '9') count++; return count; }
int main(int argc, char **argv) {
    struct node *head = NULL, **tail = &head;
    if (argc == 2) for (int i = 0; argv[1][i] != '\0'; i++) { *tail = malloc(sizeof **tail); (*tail)->value = argv[1][i]; (*tail)->next = NULL; tail = &(*tail)->next; }
    printf("%d\n", count_digits(head)); while (head != NULL) { struct node *next = head->next; free(head); head = next; } return 0;
}

