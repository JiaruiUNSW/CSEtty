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
static int solve(const struct node *head, int target) {
    long sum = 0;
        int index = 0;
        for (const struct node *p = head; p != NULL; p = p->next) {
            sum += p->data;
            if (sum >= target) return index;
            index++;
        }
        return -1;
}

int main(int argc, char **argv) {
    if (argc < 2) return 2;
    int target = atoi(argv[1]);
    struct node *head = build_list(argc, argv, 2);
    printf("%d\n", solve(head, target));
    free_list(head);
    return 0;
}
