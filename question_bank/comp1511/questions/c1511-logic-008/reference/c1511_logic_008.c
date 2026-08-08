#include <stdio.h>
static long long solve(int a,int b,int c){int r=a;long long ar=a<0?-(long long)a:a,br=b<0?-(long long)b:b,cr=c<0?-(long long)c:c;if(br<ar||(br==ar&&b<r)){r=b;ar=br;}if(cr<ar||(cr==ar&&c<r))r=c;return r;}
int main(void){int a,b,c;if(scanf("%d%d%d",&a,&b,&c)!=3)return 1;printf("result: %lld\n",solve(a,b,c));return 0;}
