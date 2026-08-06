#include <stdio.h>

enum direction { NORTH, EAST, SOUTH, WEST };

static enum direction parse_direction(char ch) {
    if (ch == 'N') return NORTH;
    if (ch == 'E') return EAST;
    if (ch == 'S') return SOUTH;
    return WEST;
}

static char direction_char(enum direction direction) {
    const char symbols[] = {'N', 'E', 'S', 'W'};
    return symbols[direction];
}

int main(void) {
    char ch;
    int turns;
    if (scanf(" %c %d", &ch, &turns) != 2) return 1;
    int rotated = ((int)parse_direction(ch) + turns) % 4;
    if (rotated < 0) rotated += 4;
    printf("direction: %c\n", direction_char((enum direction)rotated));
    return 0;
}

