#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main(int argc, char **argv) {
    if (argc != 2) return 1;
    int fd = open(argv[1], O_RDONLY); if (fd < 0) return 1;
    char buffer[4096], last = '\n'; ssize_t count; long lines = 0, bytes = 0;
    while ((count = read(fd, buffer, sizeof buffer)) > 0) { bytes += count; for (ssize_t i = 0; i < count; i++) if (buffer[i] == '\n') lines++; last = buffer[count - 1]; }
    close(fd); if (count < 0) return 1; if (bytes > 0 && last != '\n') lines++; printf("%ld\n", lines); return 0;
}

