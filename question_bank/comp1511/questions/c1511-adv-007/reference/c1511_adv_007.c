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
static struct node *keep_first_occurrences(struct node *head) {
    for (struct node *p = head; p != NULL; p = p->next) {
            struct node **link = &p->next;
            while (*link != NULL) {
                if ((*link)->data == p->data) {
                    struct node *removed = *link;
                    *link = removed->next;
                    free(removed);
                } else {
                    link = &(*link)->next;
                }
            }
        }
        return head;
}

int main(int argc, char **argv) {
    struct node *head = build_list(argc, argv, 1);
    head = keep_first_occurrences(head);
    print_list(head);
    free_list(head);
    return 0;
}
