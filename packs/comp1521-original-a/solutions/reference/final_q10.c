#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

static int write_all(int fd, const void *data, size_t size) {
    const unsigned char *cursor = data;
    while (size > 0) {
        ssize_t written = write(fd, cursor, size);
        if (written < 0) {
            if (errno == EINTR) {
                continue;
            }
            return -1;
        }
        cursor += written;
        size -= (size_t)written;
    }
    return 0;
}

static int read_all(int fd, void *data, size_t size) {
    unsigned char *cursor = data;
    while (size > 0) {
        ssize_t received = read(fd, cursor, size);
        if (received < 0) {
            if (errno == EINTR) {
                continue;
            }
            return -1;
        }
        if (received == 0) {
            return -1;
        }
        cursor += received;
        size -= (size_t)received;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        return 1;
    }
    long n = strtol(argv[1], NULL, 10);
    int descriptors[2];
    if (pipe(descriptors) != 0) {
        return 1;
    }

    pid_t child = fork();
    if (child < 0) {
        close(descriptors[0]);
        close(descriptors[1]);
        return 1;
    }
    if (child == 0) {
        close(descriptors[0]);
        long sum = 0;
        for (long value = 1; value <= n; value++) {
            sum += value;
        }
        int result = write_all(descriptors[1], &sum, sizeof sum);
        close(descriptors[1]);
        _exit(result == 0 ? 0 : 1);
    }

    close(descriptors[1]);
    long sum;
    int read_result = read_all(descriptors[0], &sum, sizeof sum);
    close(descriptors[0]);
    int status;
    if (waitpid(child, &status, 0) != child || read_result != 0 ||
        !WIFEXITED(status) || WEXITSTATUS(status) != 0) {
        return 1;
    }
    printf("%ld\n", sum);
    return 0;
}
