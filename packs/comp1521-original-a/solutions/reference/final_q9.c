#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
struct task { long first, last, sum; };
void *sum_range(void *argument) { struct task *task = argument; task->sum = 0; for (long i = task->first; i <= task->last; i++) task->sum += i; return NULL; }
int main(int argc, char **argv) { if (argc != 2) return 1; long n = strtol(argv[1], NULL, 10); struct task tasks[2] = {{1, n / 2, 0}, {n / 2 + 1, n, 0}}; pthread_t threads[2]; for (int i = 0; i < 2; i++) if (pthread_create(&threads[i], NULL, sum_range, &tasks[i]) != 0) return 1; for (int i = 0; i < 2; i++) if (pthread_join(threads[i], NULL) != 0) return 1; printf("%ld\n", tasks[0].sum + tasks[1].sum); return 0; }

