#include <stdio.h>
static long long solve(int a,int b,int c){if((a<=b&&b<=c)||(c<=b&&b<=a))return b;if((b<=a&&a<=c)||(c<=a&&a<=b))return a;return c;}
int main(void){int a,b,c;if(scanf("%d%d%d",&a,&b,&c)!=3)return 1;printf("result: %lld\n",solve(a,b,c));return 0;}
