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

static int compare_from_ends(const struct node *right, const struct node **left) {
    if (right == NULL) return 1;
    if (!compare_from_ends(right->next, left)) return 0;
    int equal = (*left)->data == right->data;
    *left = (*left)->next;
    return equal;
}

static int is_mirror_sequence(const struct node *head) {
    const struct node *left = head;
    return compare_from_ends(head, &left);
}

int main(int argc, char **argv) {
    struct node *head = build_list(argv, 1, argc);
    puts(is_mirror_sequence(head) ? "YES" : "NO");
    free_list(head);
    return 0;
}
