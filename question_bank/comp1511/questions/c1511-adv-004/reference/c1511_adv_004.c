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

static void free_list(struct node *head) {
    while (head != NULL) {
        struct node *next = head->next;
        free(head);
        head = next;
    }
}

/* Reference implementation. */
static int longest_nondecreasing_run(const struct node *head) {
    int current = 0;
        int best = 0;
        const struct node *previous = NULL;
        for (const struct node *p = head; p != NULL; p = p->next) {
            current = previous != NULL && p->data >= previous->data ? current + 1 : 1;
            if (current > best) best = current;
            previous = p;
        }
        return best;
}

int main(int argc, char **argv) {
    struct node *head = build_list(argc, argv, 1);
    printf("%d\n", longest_nondecreasing_run(head));
    free_list(head);
    return 0;
}
