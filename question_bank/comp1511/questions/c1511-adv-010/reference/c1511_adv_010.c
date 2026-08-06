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
    for (struct node *p = head; p != NULL; p = p->next) {
            int total = p->data;
            while (p->next != NULL && (p->next->data < 0) == (p->data < 0)) {
                struct node *removed = p->next;
                total += removed->data;
                p->next = removed->next;
                free(removed);
            }
            p->data = total;
        }
        return head;
}

int main(int argc, char **argv) {
    struct node *head = build_list(argc, argv, 1);
    head = solve(head);
    print_list(head);
    free_list(head);
    return 0;
}
