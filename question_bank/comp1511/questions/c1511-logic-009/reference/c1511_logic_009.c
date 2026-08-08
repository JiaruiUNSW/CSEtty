#include <stdio.h>
static long long solve(int a,int b,int c){int lo=a,hi=a;if(b<lo)lo=b;if(c<lo)lo=c;if(b>hi)hi=b;if(c>hi)hi=c;return (long long)hi-lo;}
int main(void){int a,b,c;if(scanf("%d%d%d",&a,&b,&c)!=3)return 1;printf("result: %lld\n",solve(a,b,c));return 0;}
