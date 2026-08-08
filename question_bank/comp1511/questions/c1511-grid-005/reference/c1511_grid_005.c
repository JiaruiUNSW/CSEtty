#include <stdio.h>
static long long solve(const int*a,int r,int c){long long x=0;for(int i=0;i<r;i++)for(int j=0;j<c;j++){int v=a[i*c+j],ok=(r*c>1);if(i&&a[(i-1)*c+j]>=v)ok=0;if(i+1<r&&a[(i+1)*c+j]>=v)ok=0;if(j&&a[i*c+j-1]>=v)ok=0;if(j+1<c&&a[i*c+j+1]>=v)ok=0;if(ok)x++;}return x;}
int main(void){int r,c,a[64];if(scanf("%d%d",&r,&c)!=2||r<0||c<0||r>8||c>8)return 1;for(int i=0;i<r*c;i++)if(scanf("%d",&a[i])!=1)return 1;printf("result: %lld\n",solve(a,r,c));return 0;}
