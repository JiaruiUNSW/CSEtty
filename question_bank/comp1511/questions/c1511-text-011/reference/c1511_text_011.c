#include <ctype.h>
#include <stdio.h>
#include <string.h>
static long long solve(const char*s){long long r=0;int prev=0;for(int i=0;s[i];i++){int now=isupper((unsigned char)s[i])?1:islower((unsigned char)s[i])?2:0;if(now&&prev&&now!=prev)r++;if(now)prev=now;}return r;}
int main(void){char line[256];if(!fgets(line,sizeof line,stdin))return 1;line[strcspn(line,"\n")]='\0';printf("result: %lld\n",solve(line));return 0;}
