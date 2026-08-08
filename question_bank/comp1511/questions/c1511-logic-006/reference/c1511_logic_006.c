#include <stdio.h>
static long long solve(int a,int b,int c){return b-a==c-b;}
int main(void){int a,b,c;if(scanf("%d%d%d",&a,&b,&c)!=3)return 1;printf("result: %lld\n",solve(a,b,c));return 0;}
