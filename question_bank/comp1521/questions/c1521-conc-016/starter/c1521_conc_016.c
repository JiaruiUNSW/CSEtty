#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s FILE THREADS\n", argv[0]);
        return 1;
    }
    // TODO: count byte slices locally and merge under a mutex.
    return 0;
}
