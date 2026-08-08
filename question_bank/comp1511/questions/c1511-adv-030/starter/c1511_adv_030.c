#include <string.h>
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
        if (fresh == NULL)
            exit(1);
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

static struct node *weave(struct node *left, struct node *right) {
    // TODO: weave the two chains without allocation.
    (void)right;
    return left;
}

int main(int argc, char **argv) {
    int divider = -1;
    for (int i = 1; i < argc; i++)
        if (strcmp(argv[i], "--") == 0)
            divider = i;
    if (divider < 0)
        return 2;
    struct node *left = build_list(argv, 1, divider);
    struct node *right = build_list(argv, divider + 1, argc);
    struct node *result = weave(left, right);
    print_list(result);
    free_list(result);
    return 0;
}
