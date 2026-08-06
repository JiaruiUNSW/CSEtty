#include <stdio.h>
#define MAX_RUNNERS 100

struct runner {
    int bib;
    int split[3];
};

static int total(struct runner value) {
    return value.split[0] + value.split[1] + value.split[2];
}

static int range(struct runner value) {
    int minimum = value.split[0], maximum = value.split[0];
    for (int i = 1; i < 3; i++) {
        if (value.split[i] < minimum) minimum = value.split[i];
        if (value.split[i] > maximum) maximum = value.split[i];
    }
    return maximum - minimum;
}

int main(void) {
    int n;
    struct runner runners[MAX_RUNNERS];
    if (scanf("%d", &n) != 1) return 1;
    for (int i = 0; i < n; i++)
        scanf("%d %d %d %d", &runners[i].bib, &runners[i].split[0],
              &runners[i].split[1], &runners[i].split[2]);
    int fastest = 0, consistent = 0;
    for (int i = 1; i < n; i++) {
        if (total(runners[i]) < total(runners[fastest])
            || (total(runners[i]) == total(runners[fastest])
                && runners[i].bib < runners[fastest].bib))
            fastest = i;
        if (range(runners[i]) < range(runners[consistent])
            || (range(runners[i]) == range(runners[consistent])
                && runners[i].bib < runners[consistent].bib))
            consistent = i;
    }
    printf("fastest: %d %d\n", runners[fastest].bib, total(runners[fastest]));
    printf("consistent: %d %d\n", runners[consistent].bib, range(runners[consistent]));
    return 0;
}

