#define _POSIX_C_SOURCE 200809L
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s WORKERS VALUE [VALUE ...]\n", argv[0]);
        return 1;
    }
    // TODO: dispatch indexed tasks through per-worker pipes.
    return 0;
}
