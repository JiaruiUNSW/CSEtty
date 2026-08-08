#include <stdio.h>
static long long solve(const int*a,int r,int c){if(r==0||c==0)return -1;long long best=0;for(int j=0;j<c;j++)best+=a[j];int at=0;for(int i=1;i<r;i++){long long x=0;for(int j=0;j<c;j++)x+=a[i*c+j];if(x>best){best=x;at=i;}}return at;}
int main(void){int r,c,a[64];if(scanf("%d%d",&r,&c)!=2||r<0||c<0||r>8||c>8)return 1;for(int i=0;i<r*c;i++)if(scanf("%d",&a[i])!=1)return 1;printf("result: %lld\n",solve(a,r,c));return 0;}
