#include <stdio.h>
struct record{char name[32];int value;};
static long long solve(const struct record*a,int n){if(n==0)return -1;int at=0;for(int i=1;i<n;i++)if(a[i].value>a[at].value)at=i;return at;}
int main(void){int n;struct record a[50];if(scanf("%d",&n)!=1||n<0||n>50)return 1;for(int i=0;i<n;i++)if(scanf("%31s%d",a[i].name,&a[i].value)!=2)return 1;printf("result: %lld\n",solve(a,n));return 0;}
