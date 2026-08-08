#include <stdio.h>
#include <stdlib.h>
#include <string.h>
struct record{char name[32];int value;};
int main(int argc,char**argv){(void)argc;(void)argv;struct record*a=NULL;int n=0,cap=0;char cmd[16],name[32];
    while(scanf("%15s",cmd)==1&&strcmp(cmd,"END")!=0){
        if(strcmp(cmd,"TOTAL")==0){long long total=0;for(int i=0;i<n;i++)total+=a[i].value;printf("TOTAL %lld\n",total);continue;}
        if(scanf("%31s",name)!=1){free(a);return 1;}int at=-1;for(int i=0;i<n;i++)if(strcmp(a[i].name,name)==0)at=i;
        if(strcmp(cmd,"QUERY")==0){printf("%s %d\n",name,at<0?0:a[at].value);continue;}
        if(strcmp(cmd,"REMOVE")==0){if(at>=0)a[at]=a[--n];continue;}
        int value;if(scanf("%d",&value)!=1){free(a);return 1;}if(at<0){if(n==cap){cap=cap?cap*2:4;void*p=realloc(a,(size_t)cap*sizeof*a);if(!p){free(a);return 1;}a=p;}at=n++;strcpy(a[at].name,name);a[at].value=0;}
        if(strcmp(cmd,"ADD")==0)a[at].value+=value;else if(strcmp(cmd,"SET")==0)a[at].value=value;else{free(a);return 1;}
    }free(a);return 0;}
