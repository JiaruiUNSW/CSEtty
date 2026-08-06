#include <stdio.h>
int main(void) {
    int value; scanf("%d", &value);
    // TODO: print exactly negative, zero, or positive.
    if (value <= 0) printf("negative\n");
    else printf("positive\n");
    return 0;
}

