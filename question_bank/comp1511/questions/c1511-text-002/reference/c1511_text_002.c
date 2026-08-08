#include <ctype.h>
#include <stdio.h>
#include <string.h>
static long long solve(const char*s){long long r=0;for(int i=0;s[i];i++)if(isdigit((unsigned char)s[i]))r++;return r;}
int main(void){char line[256];if(!fgets(line,sizeof line,stdin))return 1;line[strcspn(line,"\n")]='\0';printf("result: %lld\n",solve(line));return 0;}
