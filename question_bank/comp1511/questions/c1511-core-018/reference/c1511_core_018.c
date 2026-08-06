#include <stdio.h>
#define MAX_WORD 100

static int is_vowel(char ch) {
    return ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u';
}

int main(void) {
    char word[MAX_WORD + 1];
    if (scanf("%100s", word) != 1) return 1;
    int length = 0, vowels = 0;
    while (word[length] != '\0') {
        if (is_vowel(word[length])) vowels++;
        length++;
    }
    int bookended = is_vowel(word[0]) && is_vowel(word[length - 1]);
    printf("vowels: %d\nbookended: %s\n", vowels, bookended ? "yes" : "no");
    return 0;
}

