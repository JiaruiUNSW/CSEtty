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

int main(void) {
    // TODO: implement the complete labelled-summary processor.
    char command[16];
    while (scanf("%15s", command) == 1) {
        if (strcmp(command, "END") == 0)
            break;
    }
    return 0;
}
