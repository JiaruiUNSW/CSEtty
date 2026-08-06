#define _POSIX_C_SOURCE 200809L
#include <stdio.h>

int main(int argc, char **argv) {
    // TODO: implement normal mode and the --worker exec target.
    if (argc < 2) {
        fprintf(stderr, "usage: %s VALUE [VALUE ...]\n", argv[0]);
        return 1;
    }
    return 0;
}
