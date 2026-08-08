#include <ctype.h>
#include <stdio.h>
#include <string.h>
static long long solve(const char*s){if(!s[0])return 0;long long r=1;for(int i=1;s[i];i++)if(s[i]!=s[i-1])r++;return r;}
int main(void){char line[256];if(!fgets(line,sizeof line,stdin))return 1;line[strcspn(line,"\n")]='\0';printf("result: %lld\n",solve(line));return 0;}
