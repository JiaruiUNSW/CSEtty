#include <stdio.h>
#define MAX_WORD 100

int main(void) {
    char word[MAX_WORD + 1];
    int counts[26] = {0};
    if (scanf("%100s", word) != 1) return 1;
    for (int i = 0; word[i] != '\0'; i++) counts[word[i] - 'a']++;
    int distinct = 0;
    for (int i = 0; i < 26; i++) {
        if (counts[i] > 0) {
            printf("%c: %d\n", 'a' + i, counts[i]);
            distinct++;
        }
    }
    printf("distinct: %d\n", distinct);
    return 0;
}

