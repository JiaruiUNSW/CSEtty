#include <stdio.h>
#include <stdlib.h>

struct node {
    int data;
    struct node *next;
};

static struct node *build_list(char **argv, int start, int end) {
    struct node *head = NULL;
    struct node **tail = &head;
    for (int i = start; i < end; i++) {
        struct node *fresh = malloc(sizeof *fresh);
        if (fresh == NULL) exit(1);
        fresh->data = atoi(argv[i]);
        fresh->next = NULL;
        *tail = fresh;
        tail = &fresh->next;
    }
    return head;
}

static void print_list(const struct node *head) {
    if (head == NULL) { puts("EMPTY"); return; }
    for (const struct node *p = head; p != NULL; p = p->next) {
        printf("%s%d", p == head ? "" : " ", p->data);
    }
    putchar('\n');
}

static void free_list(struct node *head) {
    while (head != NULL) {
        struct node *next = head->next;
        free(head);
        head = next;
    }
}

static struct node *copy_from(const struct node *head, struct node *accumulator) {
    if (head == NULL) return accumulator;
    struct node *fresh = malloc(sizeof *fresh);
    if (fresh == NULL) exit(1);
    fresh->data = head->data;
    fresh->next = accumulator;
    return copy_from(head->next, fresh);
}

static struct node *solve(const struct node *head) {
    return copy_from(head, NULL);
}

int main(int argc, char **argv) {
    struct node *input = build_list(argv, 1, argc);
    struct node *result = solve(input);
    print_list(result);
    free_list(result);
    free_list(input);
    return 0;
}
