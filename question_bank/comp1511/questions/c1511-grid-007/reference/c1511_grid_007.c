#include <stdio.h>
static long long solve(const int*a,int r,int c){if(r<2||c<2)return 0;long long best=(long long)a[0]+a[1]+a[c]+a[c+1];for(int i=0;i+1<r;i++)for(int j=0;j+1<c;j++){long long x=(long long)a[i*c+j]+a[i*c+j+1]+a[(i+1)*c+j]+a[(i+1)*c+j+1];if(x>best)best=x;}return best;}
int main(void){int r,c,a[64];if(scanf("%d%d",&r,&c)!=2||r<0||c<0||r>8||c>8)return 1;for(int i=0;i<r*c;i++)if(scanf("%d",&a[i])!=1)return 1;printf("result: %lld\n",solve(a,r,c));return 0;}
