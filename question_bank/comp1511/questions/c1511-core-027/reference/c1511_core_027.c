#include <stdio.h>

int main(void) {
    int a, b, c;
    if (scanf("%d %d %d", &a, &b, &c) != 3) return 1;
    const char *label;
    if (a + b <= c || a + c <= b || b + c <= a) label = "invalid";
    else if (a == b && b == c) label = "equilateral";
    else if (a == b || a == c || b == c) label = "isosceles";
    else label = "scalene";
    printf("triangle: %s\n", label);
    return 0;
}

