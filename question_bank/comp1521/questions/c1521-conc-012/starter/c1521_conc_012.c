#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc < 2 || argc > 9) {
        fprintf(stderr, "usage: %s STRING [STRING ...]\n", argv[0]);
        return 1;
    }
    // TODO: update a shared letter histogram under a mutex.
    return 0;
}
