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
        if (fresh == NULL)
            exit(1);
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

// TODO: modify only this function.
static int first_prefix_at_least(const struct node *head, int target) {
    (void)head;
    (void)target;
    return -1;
}

int main(int argc, char **argv) {
    if (argc < 2)
        return 2;
    int target = atoi(argv[1]);
    struct node *head = build_list(argc, argv, 2);
    printf("%d\n", first_prefix_at_least(head, target));
    free_list(head);
    return 0;
}
