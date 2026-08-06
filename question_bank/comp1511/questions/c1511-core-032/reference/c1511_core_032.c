#include <stdio.h>
#define MAX_STUDENTS 100

struct student {
    int id;
    int before;
    int after;
};

static int gain(struct student value) {
    return value.after - value.before;
}

static int better(struct student candidate, struct student best) {
    int candidate_gain = gain(candidate);
    int best_gain = gain(best);
    if (candidate_gain != best_gain) return candidate_gain > best_gain;
    if (candidate.after != best.after) return candidate.after > best.after;
    return candidate.id < best.id;
}

int main(void) {
    int n;
    struct student students[MAX_STUDENTS];
    if (scanf("%d", &n) != 1) return 1;
    for (int i = 0; i < n; i++)
        scanf("%d %d %d", &students[i].id, &students[i].before, &students[i].after);
    struct student best = students[0];
    for (int i = 1; i < n; i++)
        if (better(students[i], best)) best = students[i];
    printf("student: %d\ngain: %d\n", best.id, gain(best));
    return 0;
}

