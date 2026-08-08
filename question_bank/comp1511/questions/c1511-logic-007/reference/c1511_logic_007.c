#include <stdio.h>
static long long solve(int a,int b,int c){if(a<=b&&b<=c)return 1;if(a>=b&&b>=c)return -1;return 0;}
int main(void){int a,b,c;if(scanf("%d%d%d",&a,&b,&c)!=3)return 1;printf("result: %lld\n",solve(a,b,c));return 0;}
