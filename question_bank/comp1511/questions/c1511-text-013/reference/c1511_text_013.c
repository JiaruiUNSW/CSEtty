#include <ctype.h>
#include <stdio.h>
#include <string.h>
static long long solve(const char*s){long long best=0,run=0;for(int i=0;;i++){if(s[i]&&!isspace((unsigned char)s[i]))run++;else{if(run>best)best=run;run=0;if(!s[i])break;}}return best;}
int main(void){char line[256];if(!fgets(line,sizeof line,stdin))return 1;line[strcspn(line,"\n")]='\0';printf("result: %lld\n",solve(line));return 0;}
