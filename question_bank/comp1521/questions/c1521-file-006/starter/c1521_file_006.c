#define _POSIX_C_SOURCE 200809L

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static long long solve(const unsigned char *data, size_t n) {
    // TODO: Implement this function.
    (void)data;
    (void)n;
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        return 1;
    }

    int fd = open(argv[1], O_RDONLY);
    if (fd < 0) {
        return 1;
    }

    size_t n = 0;
    size_t capacity = 256;
    unsigned char *data = malloc(capacity);
    if (data == NULL) {
        close(fd);
        return 1;
    }

    for (;;) {
        if (n == capacity) {
            capacity *= 2;
            void *resized = realloc(data, capacity);
            if (resized == NULL) {
                free(data);
                close(fd);
                return 1;
            }
            data = resized;
        }

        ssize_t bytes_read = read(fd, data + n, capacity - n);
        if (bytes_read < 0) {
            free(data);
            close(fd);
            return 1;
        }
        if (bytes_read == 0) {
            break;
        }
        n += (size_t)bytes_read;
    }

    close(fd);
    printf("result: %lld\n", solve(data, n));
    free(data);
    return 0;
}
