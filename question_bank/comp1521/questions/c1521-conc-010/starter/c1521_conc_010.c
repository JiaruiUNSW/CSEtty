#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s N THREADS\n", argv[0]);
        return 1;
    }
    // TODO: partition 1..N across threads and join them.
    return 0;
}
