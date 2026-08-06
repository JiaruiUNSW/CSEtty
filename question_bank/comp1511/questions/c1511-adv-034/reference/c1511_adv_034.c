#include <stdio.h>
#include <string.h>

#define MAX_CATEGORIES 32
#define MAX_HISTORY 100
#define NAME_SIZE 21

struct counter {
    char name[NAME_SIZE];
    int count;
};

static int find_counter(const struct counter counters[], int used, const char *name) {
    for (int i = 0; i < used; i++) if (strcmp(counters[i].name, name) == 0) return i;
    return -1;
}

int main(void) {
    struct counter counters[MAX_CATEGORIES];
    char history[MAX_HISTORY][NAME_SIZE];
    int used = 0;
    int history_length = 0;
    char command[16];
    while (scanf("%15s", command) == 1) {
        if (strcmp(command, "END") == 0) break;
        if (strcmp(command, "LOG") == 0) {
            char name[NAME_SIZE];
            if (scanf("%20s", name) != 1) return 2;
            int index = find_counter(counters, used, name);
            if (index < 0) {
                index = used++;
                strcpy(counters[index].name, name);
                counters[index].count = 0;
            }
            counters[index].count++;
            strcpy(history[history_length++], name);
        } else if (strcmp(command, "UNDO") == 0) {
            if (history_length == 0) {
                puts("NOTHING");
            } else {
                const char *name = history[--history_length];
                int index = find_counter(counters, used, name);
                counters[index].count--;
                printf("UNDONE %s\n", name);
            }
        } else if (strcmp(command, "COUNT") == 0) {
            char name[NAME_SIZE];
            if (scanf("%20s", name) != 1) return 2;
            int index = find_counter(counters, used, name);
            printf("%s %d\n", name, index < 0 ? 0 : counters[index].count);
        } else if (strcmp(command, "TOTAL") == 0) {
            printf("TOTAL %d\n", history_length);
        }
    }
    return 0;
}
