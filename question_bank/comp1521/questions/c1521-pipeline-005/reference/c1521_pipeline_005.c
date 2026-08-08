#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>
#define MODE 4
int main(void){int n,values[100];if(scanf("%d",&n)!=1||n<0||n>100)return 1;for(int i=0;i<n;i++)if(scanf("%d",&values[i])!=1)return 1;int p[2];if(pipe(p)!=0)return 1;pid_t pid=fork();if(pid<0)return 1;if(pid==0){close(p[0]);long long result=0;for(int i=0;i<n;i++){int x=values[i];if(MODE==0)result+=x;else if(MODE==1)result+=x>0;else if(MODE==2)result+=(x&1)==0;else if(MODE==3)result+=x<0?-(long long)x:x;else result+=(long long)(i+1)*x;}if(write(p[1],&result,sizeof result)!=(ssize_t)sizeof result)_exit(2);close(p[1]);_exit(0);}close(p[1]);long long result;if(read(p[0],&result,sizeof result)!=(ssize_t)sizeof result)return 1;close(p[0]);int status;if(waitpid(pid,&status,0)<0||!WIFEXITED(status)||WEXITSTATUS(status)!=0)return 1;printf("result: %lld\n",result);return 0;}
