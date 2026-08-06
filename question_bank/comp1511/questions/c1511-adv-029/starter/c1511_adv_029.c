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

static int solve(const struct node *head) {
    /* TODO: recursively compare mirrored positions. */
    (void)head;
    return 0;
}

int main(int argc, char **argv) {
    struct node *head = build_list(argv, 1, argc);
    puts(solve(head) ? "YES" : "NO");
    free_list(head);
    return 0;
}
