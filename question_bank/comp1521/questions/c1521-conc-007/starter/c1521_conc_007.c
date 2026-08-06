#define _POSIX_C_SOURCE 200809L
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc < 2 || argc > 9) {
        fprintf(stderr, "usage: %s CODE [CODE ...]\n", argv[0]);
        return 1;
    }
    // TODO: fork children and report decoded exit statuses.
    return 0;
}
