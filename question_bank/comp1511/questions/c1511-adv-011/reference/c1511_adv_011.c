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
static struct node *solve(struct node *head) {
    if (head == NULL || head->next == NULL) return head;
        struct node *slow = head;
        struct node *fast = head->next;
        while (fast != NULL && fast->next != NULL) {
            slow = slow->next;
            fast = fast->next->next;
        }
        struct node *second = slow->next;
        slow->next = NULL;
        struct node *reversed = NULL;
        while (second != NULL) {
            struct node *next = second->next;
            second->next = reversed;
            reversed = second;
            second = next;
        }
        struct node *first = head;
        while (reversed != NULL) {
            struct node *first_next = first->next;
            struct node *second_next = reversed->next;
            first->next = reversed;
            reversed->next = first_next;
            first = first_next;
            reversed = second_next;
        }
        return head;
}

int main(int argc, char **argv) {
    struct node *head = build_list(argc, argv, 1);
    head = solve(head);
    print_list(head);
    free_list(head);
    return 0;
}
