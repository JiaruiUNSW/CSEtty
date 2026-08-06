#include <stdio.h>
int main(void) { int value; scanf("%d", &value); if (value < 0) puts("negative"); else if (value == 0) puts("zero"); else puts("positive"); return 0; }

