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

static struct node *solve(struct node *head, int threshold) {
    (void)threshold;
        return head;
}

int main(int argc, char **argv) {
    if (argc < 2) return 2;
    struct node *head = build_list(argv, 2, argc);
    head = solve(head, atoi(argv[1]));
    print_list(head);
    free_list(head);
    return 0;
}
