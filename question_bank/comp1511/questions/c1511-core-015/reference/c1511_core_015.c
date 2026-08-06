#include <stdio.h>

enum signal { RED, GREEN, AMBER };

static enum signal advance(enum signal state) {
    if (state == RED) return GREEN;
    if (state == GREEN) return AMBER;
    return RED;
}

static char state_char(enum signal state) {
    if (state == RED) return 'R';
    if (state == GREEN) return 'G';
    return 'A';
}

int main(void) {
    char input;
    int steps;
    if (scanf(" %c %d", &input, &steps) != 2) return 1;
    enum signal state = input == 'R' ? RED : (input == 'G' ? GREEN : AMBER);
    for (int i = 0; i < steps; i++) state = advance(state);
    printf("state: %c\n", state_char(state));
    return 0;
}

