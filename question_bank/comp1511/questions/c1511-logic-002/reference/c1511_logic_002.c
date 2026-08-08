#include <stdio.h>
static long long solve(int a,int b,int c){if(a<=0||b<=0||c<=0||a+b<=c||a+c<=b||b+c<=a)return 0;if(a==b&&b==c)return 3;if(a==b||b==c||a==c)return 2;return 1;}
int main(void){int a,b,c;if(scanf("%d%d%d",&a,&b,&c)!=3)return 1;printf("result: %lld\n",solve(a,b,c));return 0;}
