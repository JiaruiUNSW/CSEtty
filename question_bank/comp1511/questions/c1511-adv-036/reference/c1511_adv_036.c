#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NAME_SIZE 21

struct node {
    char name[NAME_SIZE];
    struct node *next;
};

static struct node *new_node(const char *name) {
    struct node *fresh = malloc(sizeof *fresh);
    if (fresh == NULL) exit(1);
    strcpy(fresh->name, name);
    fresh->next = NULL;
    return fresh;
}

static void append(struct node **head, const char *name) {
    struct node **tail = head;
    while (*tail != NULL) tail = &(*tail)->next;
    *tail = new_node(name);
}

static void prepend(struct node **head, const char *name) {
    struct node *fresh = new_node(name);
    fresh->next = *head;
    *head = fresh;
}

static int remove_first(struct node **head, const char *name) {
    struct node **link = head;
    while (*link != NULL && strcmp((*link)->name, name) != 0) link = &(*link)->next;
    if (*link == NULL) return 0;
    struct node *removed = *link;
    *link = removed->next;
    free(removed);
    return 1;
}

static void reverse(struct node **head) {
    struct node *result = NULL;
    while (*head != NULL) {
        struct node *next = (*head)->next;
        (*head)->next = result;
        result = *head;
        *head = next;
    }
    *head = result;
}

static void print_chain(const struct node *head) {
    if (head == NULL) { puts("EMPTY"); return; }
    for (const struct node *p = head; p != NULL; p = p->next) {
        printf("%s%s", p == head ? "" : " -> ", p->name);
    }
    putchar('\n');
}

static void destroy(struct node *head) {
    while (head != NULL) {
        struct node *next = head->next;
        free(head);
        head = next;
    }
}

int main(void) {
    struct node *head = NULL;
    char command[16];
    while (scanf("%15s", command) == 1) {
        if (strcmp(command, "END") == 0) break;
        if (strcmp(command, "APPEND") == 0 || strcmp(command, "PREPEND") == 0) {
            char name[NAME_SIZE];
            if (scanf("%20s", name) != 1) return 2;
            if (command[0] == 'A') append(&head, name);
            else prepend(&head, name);
        } else if (strcmp(command, "REMOVE") == 0) {
            char name[NAME_SIZE];
            if (scanf("%20s", name) != 1) return 2;
            printf("%s %s\n", remove_first(&head, name) ? "REMOVED" : "MISSING", name);
        } else if (strcmp(command, "REVERSE") == 0) {
            reverse(&head);
        } else if (strcmp(command, "PRINT") == 0) {
            print_chain(head);
        }
    }
    destroy(head);
    return 0;
}
