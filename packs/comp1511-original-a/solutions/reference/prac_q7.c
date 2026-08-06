#include <stdio.h>
void swap(int *left, int *right) { int temporary = *left; *left = *right; *right = temporary; }
int main(void) { int a, b; scanf("%d %d", &a, &b); swap(&a, &b); printf("%d %d\n", a, b); return 0; }

