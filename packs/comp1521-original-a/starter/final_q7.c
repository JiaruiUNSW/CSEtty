#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        return 1;
    }
    int requested = atoi(argv[1]);
    // TODO: fork, make the child exit with requested, wait, and print its status.
    printf("%d\n", requested);
    return 0;
}
