#include <ctype.h>
#include <stdio.h>
#include <string.h>
static long long solve(const char*s){long long depth=0,best=0;for(int i=0;s[i];i++){if(s[i]=='('){depth++;if(depth>best)best=depth;}else if(s[i]==')'){depth--;if(depth<0)return -1;}}return depth==0?best:-1;}
int main(void){char line[256];if(!fgets(line,sizeof line,stdin))return 1;line[strcspn(line,"\n")]='\0';printf("result: %lld\n",solve(line));return 0;}
