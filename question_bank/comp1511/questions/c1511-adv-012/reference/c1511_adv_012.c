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


/* Reference implementation. */
static int consume_checksum(struct node *head) {
    int total = 0;
        int sign = 1;
        while (head != NULL) {
            struct node *next = head->next;
            total += sign * head->data;
            sign = -sign;
            free(head);
            head = next;
        }
        return total;
}

int main(int argc, char **argv) {
    struct node *head = build_list(argc, argv, 1);
    printf("%d\n", consume_checksum(head));
    return 0;
}
