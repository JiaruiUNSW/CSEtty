#define _POSIX_C_SOURCE 200809L
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s FILE\n", argv[0]);
        return 1;
    }
    // TODO: fork the scanner and collect line offsets.
    return 0;
}

