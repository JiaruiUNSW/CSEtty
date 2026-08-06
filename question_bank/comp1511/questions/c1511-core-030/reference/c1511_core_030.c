#include <stdio.h>
#define MAX_LINE 200

static char uppercase(char ch) {
    if (ch >= 'a' && ch <= 'z') return (char)(ch - 'a' + 'A');
    return ch;
}

static int separator(char ch) {
    return ch == ' ' || ch == '\t' || ch == '\n';
}

int main(void) {
    char line[MAX_LINE + 2];
    char initials[MAX_LINE + 1];
    if (fgets(line, sizeof line, stdin) == NULL) return 1;
    int in_word = 0, words = 0;
    for (int i = 0; line[i] != '\0'; i++) {
        if (separator(line[i])) {
            in_word = 0;
        } else if (!in_word) {
            initials[words] = uppercase(line[i]);
            words++;
            in_word = 1;
        }
    }
    initials[words] = '\0';
    printf("initials: %s\nwords: %d\n", initials, words);
    return 0;
}

