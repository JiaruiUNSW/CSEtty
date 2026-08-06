#include <stdio.h>
#include <string.h>

#define MAX_RECORDS 32
#define NAME_SIZE 21

struct record {
    char name[NAME_SIZE];
    int quantity;
};

static int find_record(const struct record records[], int count, const char *name) {
    for (int i = 0; i < count; i++) {
        if (strcmp(records[i].name, name) == 0) return i;
    }
    return -1;
}

int main(void) {
    struct record records[MAX_RECORDS];
    int count = 0;
    char command[16];
    while (scanf("%15s", command) == 1) {
        if (strcmp(command, "END") == 0) break;
        if (strcmp(command, "ADD") == 0) {
            char name[NAME_SIZE];
            int amount;
            if (scanf("%20s %d", name, &amount) != 2) return 2;
            int index = find_record(records, count, name);
            if (index < 0) {
                index = count++;
                strcpy(records[index].name, name);
                records[index].quantity = 0;
            }
            records[index].quantity += amount;
        } else if (strcmp(command, "TAKE") == 0) {
            char name[NAME_SIZE];
            int amount;
            if (scanf("%20s %d", name, &amount) != 2) return 2;
            int index = find_record(records, count, name);
            if (index < 0 || records[index].quantity < amount) {
                printf("REJECTED %s\n", name);
            } else {
                records[index].quantity -= amount;
                printf("TAKEN %s %d\n", name, records[index].quantity);
            }
        } else if (strcmp(command, "SHOW") == 0) {
            int printed = 0;
            for (int i = 0; i < count; i++) {
                if (records[i].quantity > 0) {
                    printf("%s %d\n", records[i].name, records[i].quantity);
                    printed = 1;
                }
            }
            if (!printed) puts("EMPTY");
            puts("--");
        }
    }
    return 0;
}
