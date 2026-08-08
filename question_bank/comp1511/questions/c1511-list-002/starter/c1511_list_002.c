#include <stdio.h>
#include <stdlib.h>

struct node {
    int value;
    struct node *next;
};

static long long solve(const struct node *head) {
    // TODO: Implement this function.
    (void)head;
    return 0;
}

int main(int argc, char **argv) {
    struct node *head = NULL;
    struct node **tail = &head;

    for (int i = 1; i < argc; i++) {
        struct node *node = malloc(sizeof *node);
        if (node == NULL) {
            return 1;
        }
        node->value = atoi(argv[i]);
        node->next = NULL;
        *tail = node;
        tail = &node->next;
    }

    printf("result: %lld\n", solve(head));

    while (head != NULL) {
        struct node *next = head->next;
        free(head);
        head = next;
    }
    return 0;
}
