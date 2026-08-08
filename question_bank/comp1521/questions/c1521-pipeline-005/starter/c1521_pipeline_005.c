#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

#define MODE 4

int main(void) {
    int n;
    int values[100];

    if (scanf("%d", &n) != 1 || n < 0 || n > 100) {
        return 1;
    }
    for (int i = 0; i < n; i++) {
        if (scanf("%d", &values[i]) != 1) {
            return 1;
        }
    }

    int pipe_fds[2];
    if (pipe(pipe_fds) != 0) {
        return 1;
    }

    pid_t pid = fork();
    if (pid < 0) {
        return 1;
    }
    if (pid == 0) {
        close(pipe_fds[0]);
        // TODO: Compute and write one complete result record.
        (void)values;
        return 1;
    }

    close(pipe_fds[1]);
    long long result;
    if (read(pipe_fds[0], &result, sizeof result) != (ssize_t)sizeof result) {
        return 1;
    }
    close(pipe_fds[0]);

    int status;
    if (waitpid(pid, &status, 0) < 0 || !WIFEXITED(status) ||
        WEXITSTATUS(status) != 0) {
        return 1;
    }

    printf("result: %lld\n", result);
    return 0;
}
