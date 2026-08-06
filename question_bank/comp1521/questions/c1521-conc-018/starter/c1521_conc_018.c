#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc < 2 || argc > 7) {
        fprintf(stderr, "usage: %s FILE [FILE ...]\n", argv[0]);
        return 1;
    }
    // TODO: scan files in threads and merge local histograms.
    return 0;
}
