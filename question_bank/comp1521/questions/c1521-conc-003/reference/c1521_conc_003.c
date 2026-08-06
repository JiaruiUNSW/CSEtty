#define _POSIX_C_SOURCE 200809L
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NODES 64
#define MAX_DEPS 32
#define NAME_SIZE 32

struct node {
    char name[NAME_SIZE];
    char dep_names[MAX_DEPS][NAME_SIZE];
    int deps[MAX_DEPS];
    int dep_count;
    int built;
};

static int find_node(struct node *nodes, int count, const char *name) {
    for (int i = 0; i < count; i++) if (strcmp(nodes[i].name, name) == 0) return i;
    return -1;
}

static int valid_name(const char *name) {
    if (*name == '\0') return 0;
    for (const unsigned char *p = (const unsigned char *)name; *p; p++) {
        if (!islower(*p) && !isdigit(*p) && *p != '_') return 0;
    }
    return strlen(name) < NAME_SIZE;
}

static struct node *sort_nodes;

static int compare_indices(const void *left, const void *right) {
    int a = *(const int *)left;
    int b = *(const int *)right;
    return strcmp(sort_nodes[a].name, sort_nodes[b].name);
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s MANIFEST\n", argv[0]);
        return 1;
    }
    FILE *input = fopen(argv[1], "r");
    if (input == NULL) { perror("fopen"); return 1; }
    static struct node nodes[MAX_NODES];
    int count = 0;
    char line[512];
    while (fgets(line, sizeof line, input) != NULL) {
        char *newline = strchr(line, '\n');
        if (newline != NULL) *newline = '\0';
        char *start = line;
        while (isspace((unsigned char)*start)) start++;
        if (*start == '\0') continue;
        char *colon = strchr(start, ':');
        if (colon == NULL || count == MAX_NODES) { fclose(input); return 1; }
        *colon = '\0';
        char *end = colon - 1;
        while (end >= start && isspace((unsigned char)*end)) *end-- = '\0';
        if (!valid_name(start) || find_node(nodes, count, start) >= 0) {
            fclose(input); return 1;
        }
        strcpy(nodes[count].name, start);
        char *save = NULL;
        char *token = strtok_r(colon + 1, " \t\r", &save);
        while (token != NULL) {
            if (!valid_name(token) || nodes[count].dep_count == MAX_DEPS) {
                fclose(input); return 1;
            }
            strcpy(nodes[count].dep_names[nodes[count].dep_count++], token);
            token = strtok_r(NULL, " \t\r", &save);
        }
        count++;
    }
    if (ferror(input) || fclose(input) != 0) return 1;
    for (int i = 0; i < count; i++) {
        for (int j = 0; j < nodes[i].dep_count; j++) {
            int dep = find_node(nodes, count, nodes[i].dep_names[j]);
            if (dep < 0) return 1;
            nodes[i].deps[j] = dep;
        }
    }
    int completed = 0;
    int wave = 0;
    sort_nodes = nodes;
    while (completed < count) {
        int ready[MAX_NODES];
        int ready_count = 0;
        for (int i = 0; i < count; i++) {
            if (nodes[i].built) continue;
            int ok = 1;
            for (int j = 0; j < nodes[i].dep_count; j++) {
                if (!nodes[nodes[i].deps[j]].built) ok = 0;
            }
            if (ok) ready[ready_count++] = i;
        }
        if (ready_count == 0) {
            puts("cycle");
            return 2;
        }
        qsort(ready, (size_t)ready_count, sizeof ready[0], compare_indices);
        printf("wave %d:", wave++);
        for (int i = 0; i < ready_count; i++) printf(" %s", nodes[ready[i]].name);
        putchar('\n');
        for (int i = 0; i < ready_count; i++) nodes[ready[i]].built = 1;
        completed += ready_count;
    }
    return 0;
}
