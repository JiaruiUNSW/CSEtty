#define _POSIX_C_SOURCE 200809L
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc < 2 || argc > 5) {
        fprintf(stderr, "usage: %s FILE [FILE ...]\n", argv[0]);
        return 1;
    }
    // TODO: fork one fingerprint worker per file.
    return 0;
}

