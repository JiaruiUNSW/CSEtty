#include <ctype.h>
#include <stdio.h>
#include <string.h>
static long long solve(const char*s){(void)s;return 0;}
int main(void){char line[256];if(!fgets(line,sizeof line,stdin))return 1;line[strcspn(line,"\n")]='\0';printf("result: %lld\n",solve(line));return 0;}
