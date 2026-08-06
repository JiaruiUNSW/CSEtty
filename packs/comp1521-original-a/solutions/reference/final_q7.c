#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        return 1;
    }
    int requested = atoi(argv[1]);
    pid_t child = fork();
    if (child < 0) {
        return 1;
    }
    if (child == 0) {
        _exit(requested & 255);
    }
    int status;
    if (waitpid(child, &status, 0) != child || !WIFEXITED(status)) {
        return 1;
    }
    printf("%d\n", WEXITSTATUS(status));
    return 0;
}
