#include <stdio.h>
#include <stdlib.h>

struct node {
    int data;
    struct node *next;
};

static struct node *build_list(int argc, char **argv, int start) {
    struct node *head = NULL;
    struct node **tail = &head;
    for (int i = start; i < argc; i++) {
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
    if (head == NULL) {
        puts("EMPTY");
        return;
    }
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

/* Reference implementation. */
static struct node *solve(struct node *head) {
    struct node *odd_head = NULL, *odd_tail = NULL;
        struct node *even_head = NULL, *even_tail = NULL;
        while (head != NULL) {
            struct node *next = head->next;
            head->next = NULL;
            struct node **group_head = head->data % 2 != 0 ? &odd_head : &even_head;
            struct node **group_tail = head->data % 2 != 0 ? &odd_tail : &even_tail;
            if (*group_tail == NULL) *group_head = head;
            else (*group_tail)->next = head;
            *group_tail = head;
            head = next;
        }
        if (odd_tail != NULL) odd_tail->next = even_head;
        return odd_head != NULL ? odd_head : even_head;
}

int main(int argc, char **argv) {
    struct node *head = build_list(argc, argv, 1);
    head = solve(head);
    print_list(head);
    free_list(head);
    return 0;
}
