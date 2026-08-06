#include <stdio.h>
int main(void) { int counts[26] = {0}, ch; while ((ch = getchar()) != EOF) if (ch >= 'a' && ch <= 'z') counts[ch - 'a']++; int best = 0; for (int i = 1; i < 26; i++) if (counts[i] > counts[best]) best = i; printf("%c %d\n", 'a' + best, counts[best]); return 0; }

