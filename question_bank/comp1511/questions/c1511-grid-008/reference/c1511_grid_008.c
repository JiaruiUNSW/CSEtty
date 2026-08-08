#include <stdio.h>
static long long solve(const int*a,int r,int c){if(r==0||c==0)return 0;int lo=a[0],hi=a[0];for(int i=1;i<r*c;i++){if(a[i]<lo)lo=a[i];if(a[i]>hi)hi=a[i];}return (long long)hi-lo;}
int main(void){int r,c,a[64];if(scanf("%d%d",&r,&c)!=2||r<0||c<0||r>8||c>8)return 1;for(int i=0;i<r*c;i++)if(scanf("%d",&a[i])!=1)return 1;printf("result: %lld\n",solve(a,r,c));return 0;}
