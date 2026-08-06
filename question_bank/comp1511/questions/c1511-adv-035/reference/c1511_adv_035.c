#include <stdio.h>
#include <string.h>

#define MAX_SUMMARIES 16
#define LABEL_SIZE 21

struct summary {
    char label[LABEL_SIZE];
    int count;
    long sum;
    int minimum;
    int maximum;
};

static int find_summary(const struct summary summaries[], int used, const char *label) {
    for (int i = 0; i < used; i++) if (strcmp(summaries[i].label, label) == 0) return i;
    return -1;
}

int main(void) {
    struct summary summaries[MAX_SUMMARIES];
    int used = 0;
    char command[16];
    while (scanf("%15s", command) == 1) {
        if (strcmp(command, "END") == 0) break;
        if (strcmp(command, "READ") == 0) {
            char label[LABEL_SIZE];
            int value;
            if (scanf("%20s %d", label, &value) != 2) return 2;
            int index = find_summary(summaries, used, label);
            if (index < 0) {
                index = used++;
                strcpy(summaries[index].label, label);
                summaries[index].count = 1;
                summaries[index].sum = value;
                summaries[index].minimum = value;
                summaries[index].maximum = value;
            } else {
                summaries[index].count++;
                summaries[index].sum += value;
                if (value < summaries[index].minimum) summaries[index].minimum = value;
                if (value > summaries[index].maximum) summaries[index].maximum = value;
            }
        } else if (strcmp(command, "STATS") == 0) {
            char label[LABEL_SIZE];
            if (scanf("%20s", label) != 1) return 2;
            int index = find_summary(summaries, used, label);
            if (index < 0) {
                printf("MISSING %s\n", label);
            } else {
                const struct summary *s = &summaries[index];
                printf("%s count=%d min=%d max=%d mean=%ld\n",
                       s->label, s->count, s->minimum, s->maximum, s->sum / s->count);
            }
        } else if (strcmp(command, "RESET") == 0) {
            char label[LABEL_SIZE];
            if (scanf("%20s", label) != 1) return 2;
            int index = find_summary(summaries, used, label);
            if (index < 0) {
                printf("MISSING %s\n", label);
            } else {
                for (int i = index; i + 1 < used; i++) summaries[i] = summaries[i + 1];
                used--;
                printf("RESET %s\n", label);
            }
        }
    }
    return 0;
}
