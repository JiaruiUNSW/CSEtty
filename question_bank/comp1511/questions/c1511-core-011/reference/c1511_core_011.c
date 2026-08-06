#include <stdio.h>
#define MAX_VALUES 100

static int compact(int values[], int n, int sentinel) {
    int write = 0;
    for (int read = 0; read < n; read++) {
        if (values[read] != sentinel) {
            values[write] = values[read];
            write++;
        }
    }
    return write;
}

int main(void) {
    int n, sentinel;
    int values[MAX_VALUES];
    if (scanf("%d %d", &n, &sentinel) != 2) return 1;
    for (int i = 0; i < n; i++) scanf("%d", &values[i]);
    int kept = compact(values, n, sentinel);
    for (int i = 0; i < kept; i++) {
        if (i > 0) printf(" ");
        printf("%d", values[i]);
    }
    printf("\nkept: %d\n", kept);
    return 0;
}

