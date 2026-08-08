#include <stdio.h>
static long long solve(int a,int b,int c){long long x=a<0?-(long long)a:a,y=b<0?-(long long)b:b,z=c<0?-(long long)c:c;return x>y?(x>z?x:z):(y>z?y:z);}
int main(void){int a,b,c;if(scanf("%d%d%d",&a,&b,&c)!=3)return 1;printf("result: %lld\n",solve(a,b,c));return 0;}
