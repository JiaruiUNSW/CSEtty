#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main(int argc, char **argv) {
    if (argc != 2) return 1;
    int fd = open(argv[1], O_RDONLY);
    if (fd < 0) return 1;
    // TODO: count logical lines using read(2), including a final unterminated line.
    close(fd);
    printf("0\n");
    return 0;
}

