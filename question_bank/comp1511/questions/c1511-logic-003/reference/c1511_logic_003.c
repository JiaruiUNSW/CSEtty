#include <stdio.h>
static long long solve(int a,int b,int c){int lo=a<c?a:c,hi=a>c?a:c;return b<lo?lo:b>hi?hi:b;}
int main(void){int a,b,c;if(scanf("%d%d%d",&a,&b,&c)!=3)return 1;printf("result: %lld\n",solve(a,b,c));return 0;}
