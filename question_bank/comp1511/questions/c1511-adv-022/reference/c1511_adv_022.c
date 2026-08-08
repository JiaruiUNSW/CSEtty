#include <ctype.h>
#include <stdio.h>

static int first_decimal(const char *text, int *value) {
    const char *p = text;
    while (*p != '\0') {
        int sign = 1;
        const char *digits = p;
        if ((*p == '+' || *p == '-') && isdigit((unsigned char)p[1])) {
            sign = *p == '-' ? -1 : 1;
            digits = p + 1;
        } else if (!isdigit((unsigned char)*p)) {
            p++;
            continue;
        }
        int result = 0;
        while (isdigit((unsigned char)*digits)) {
            result = result * 10 + (*digits - '0');
            digits++;
        }
        *value = sign * result;
        return 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int value = 0;
    if (first_decimal(argv[1], &value)) printf("%d\n", value);
    else puts("NONE");
    return 0;
}
