#include <stdio.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 1;
    for (int value = n; value >= 1; value--) {
        printf("%d", value);
        if (value > 1) printf(">");
    }
    printf("\n");
    return 0;
}

