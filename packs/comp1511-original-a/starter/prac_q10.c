#include <stdio.h>
int main(void) {
    int counts[26] = {0};
    int character;
    while ((character = getchar()) != EOF) if (character >= 'a' && character <= 'z') counts[character - 'a']++;
    // TODO: select the greatest count, resolving ties alphabetically.
    printf("a %d\n", counts[0]);
    return 0;
}

