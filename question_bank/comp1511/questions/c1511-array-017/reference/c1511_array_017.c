#include <stdio.h>
static long long solve(const int *a,int n){long long total=0,result=0; for(int i=0;i<n;i++){total+=a[i]; if(total>=0)result++;} return result;}
int main(void){
    int n;
    int values[100];
    if(scanf("%d",&n)!=1||n<0||n>100)return 1;
    for(int i=0;i<n;i++)if(scanf("%d",&values[i])!=1)return 1;
    printf("result: %lld\n",solve(values,n));
    return 0;
}
