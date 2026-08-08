#include <stdio.h>
static long long solve(const int*a,int r,int c){(void)a;(void)r;(void)c;return 0;}
int main(void){int r,c,a[64];if(scanf("%d%d",&r,&c)!=2||r<0||c<0||r>8||c>8)return 1;for(int i=0;i<r*c;i++)if(scanf("%d",&a[i])!=1)return 1;printf("result: %lld\n",solve(a,r,c));return 0;}
