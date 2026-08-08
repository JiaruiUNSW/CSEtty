#include <ctype.h>
#include <stdio.h>
#include <string.h>
static long long solve(const char*s){char clean[256];int n=0;for(int i=0;s[i]&&n<255;i++)if(isalnum((unsigned char)s[i]))clean[n++]=(char)tolower((unsigned char)s[i]);for(int i=0;i<n/2;i++)if(clean[i]!=clean[n-1-i])return 0;return 1;}
int main(void){char line[256];if(!fgets(line,sizeof line,stdin))return 1;line[strcspn(line,"\n")]='\0';printf("result: %lld\n",solve(line));return 0;}
