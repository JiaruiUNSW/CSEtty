#include <stdio.h>
static long long solve(const int *a,int n){long long result=0; for(int i=0;i<n;i++){long long x=a[i]; if(x<0)x=-x; if(x>result)result=x;} return result;}
int main(void){
    int n;
    int values[100];
    if(scanf("%d",&n)!=1||n<0||n>100)return 1;
    for(int i=0;i<n;i++)if(scanf("%d",&values[i])!=1)return 1;
    printf("result: %lld\n",solve(values,n));
    return 0;
}
