#include <ctype.h>
#include <stdio.h>
#include <string.h>
static long long solve(const char*s){for(int i=0;s[i];i++)if(isdigit((unsigned char)s[i]))return i;return -1;}
int main(void){char line[256];if(!fgets(line,sizeof line,stdin))return 1;line[strcspn(line,"\n")]='\0';printf("result: %lld\n",solve(line));return 0;}
