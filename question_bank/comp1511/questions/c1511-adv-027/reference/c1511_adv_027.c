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

static void solve(struct node *head, struct node **first, struct node **second) {
    *first = NULL;
    *second = NULL;
    struct node **first_tail = first;
    struct node **second_tail = second;
    int index = 0;
    while (head != NULL) {
        struct node *next = head->next;
        head->next = NULL;
        struct node ***tail = index % 2 == 0 ? &first_tail : &second_tail;
        **tail = head;
        *tail = &head->next;
        head = next;
        index++;
    }
}

static void print_named(const char *name, const struct node *head) {
    printf("%s: ", name);
    print_list(head);
}

int main(int argc, char **argv) {
    struct node *head = build_list(argv, 1, argc);
    struct node *first = NULL, *second = NULL;
    solve(head, &first, &second);
    print_named("A", first);
    print_named("B", second);
    free_list(first);
    free_list(second);
    return 0;
}
