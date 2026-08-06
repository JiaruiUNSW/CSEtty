#include <stdio.h>
#include <string.h>
int main(void) { int value = 0, operand; char command[16]; while (scanf("%15s", command) == 1) { if (strcmp(command, "quit") == 0) break; if (strcmp(command, "print") == 0) printf("%d\n", value); else if (strcmp(command, "add") == 0 && scanf("%d", &operand) == 1) value += operand; else if (strcmp(command, "mul") == 0 && scanf("%d", &operand) == 1) value *= operand; } return 0; }
