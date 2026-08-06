#include <stdio.h>
#define MAX_WORD 100

int main(void) {
    char word[MAX_WORD + 1];
    if (scanf("%100s", word) != 1) return 1;
    int runs = 1;
    for (int i = 1; word[i] != '\0'; i++)
        if (word[i] != word[i - 1]) runs++;
    printf("runs: %d\n", runs);
    return 0;
}

