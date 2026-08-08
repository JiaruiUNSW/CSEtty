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
static int count_record_highs(const struct node *head) {
    if (head == NULL) return 0;
        int best = head->data;
        int count = 1;
        for (const struct node *p = head->next; p != NULL; p = p->next) {
            if (p->data > best) {
                best = p->data;
                count++;
            }
        }
        return count;
}

int main(int argc, char **argv) {
    struct node *head = build_list(argc, argv, 1);
    printf("%d\n", count_record_highs(head));
    free_list(head);
    return 0;
}
