#include <stdio.h>
int longest_run(const char *text) { int best = 1, run = 1; for (int i = 1; text[i] != '\0'; i++) { if (text[i] == text[i - 1]) run++; else run = 1; if (run > best) best = run; } return best; }
int main(int argc, char **argv) { if (argc == 2) printf("%d\n", longest_run(argv[1])); return 0; }

