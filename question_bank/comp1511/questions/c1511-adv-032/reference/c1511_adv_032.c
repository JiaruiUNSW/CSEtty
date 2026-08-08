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

static void print_list(const struct node *head) {
    if (head == NULL) { puts("EMPTY"); return; }
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

static struct node *keep_even_prefixes(struct node *head, int *running_sum) {
    if (head == NULL) return NULL;
    *running_sum += head->data;
    int keep = *running_sum % 2 == 0;
    struct node *suffix = keep_even_prefixes(head->next, running_sum);
    if (keep) {
        head->next = suffix;
        return head;
    }
    free(head);
    return suffix;
}

int main(int argc, char **argv) {
    struct node *head = build_list(argv, 1, argc);
    int running_sum = 0;
    head = keep_even_prefixes(head, &running_sum);
    print_list(head);
    free_list(head);
    return 0;
}
