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
static struct node *solve(struct node *head, int value) {
    struct node *last_even = NULL;
        for (struct node *p = head; p != NULL; p = p->next) {
            if (p->data % 2 == 0) last_even = p;
        }
        struct node *fresh = malloc(sizeof *fresh);
        if (fresh == NULL) exit(1);
        fresh->data = value;
        if (last_even == NULL) {
            fresh->next = head;
            return fresh;
        }
        fresh->next = last_even->next;
        last_even->next = fresh;
        return head;
}

int main(int argc, char **argv) {
    if (argc < 2) return 2;
    int value = atoi(argv[1]);
    struct node *head = build_list(argc, argv, 2);
    head = solve(head, value);
    print_list(head);
    free_list(head);
    return 0;
}
