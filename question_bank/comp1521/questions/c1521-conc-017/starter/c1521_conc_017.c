#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "usage: %s CAPACITY CONSUMERS VALUE [VALUE ...]\n", argv[0]);
        return 1;
    }
    // TODO: implement a bounded producer/consumer queue.
    return 0;
}
