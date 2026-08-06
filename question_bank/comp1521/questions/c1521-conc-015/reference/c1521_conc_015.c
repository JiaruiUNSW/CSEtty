#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

struct task { int index; long long value; };
struct result { int index; long long value,square,cube; };

static int transfer(int fd,void *buffer,size_t size,int writing){
    unsigned char *p=buffer;
    while(size>0){
        ssize_t n=writing?write(fd,p,size):read(fd,p,size);
        if(n<0&&errno==EINTR)continue;
        if(n<=0)return -1;
        p+=(size_t)n;size-=(size_t)n;
    }
    return 0;
}

static int worker_loop(int input,int output){
    for(;;){
        struct task task;
        if(transfer(input,&task,sizeof task,0)<0)return -1;
        if(task.index<0)return 0;
        struct result result={task.index,task.value,task.value*task.value,task.value*task.value*task.value};
        ssize_t n;
        do{n=write(output,&result,sizeof result);}while(n<0&&errno==EINTR);
        if(n!=(ssize_t)sizeof result)return -1;
    }
}

int main(int argc,char **argv){
    if(argc<3||argc>18){fprintf(stderr,"usage: %s WORKERS VALUE [VALUE ...]\n",argv[0]);return 1;}
    char *end=NULL;long parsed=strtol(argv[1],&end,10);
    if(*argv[1]=='\0'||*end!='\0'||parsed<1||parsed>4)return 1;
    int workers=(int)parsed,count=argc-2;
    long long values[16];
    for(int i=0;i<count;i++){
        char *value_end=NULL;long value=strtol(argv[i+2],&value_end,10);
        if(*argv[i+2]=='\0'||*value_end!='\0'||value<-100||value>100)return 1;
        values[i]=value;
    }
    int tasks[4][2],results[2];pid_t pids[4];
    for(int i=0;i<workers;i++)if(pipe(tasks[i])<0)return 1;
    if(pipe(results)<0)return 1;
    for(int i=0;i<workers;i++){
        pids[i]=fork();if(pids[i]<0)return 1;
        if(pids[i]==0){
            for(int j=0;j<workers;j++){close(tasks[j][1]);if(j!=i)close(tasks[j][0]);}
            close(results[0]);int ok=worker_loop(tasks[i][0],results[1]);
            close(tasks[i][0]);close(results[1]);_exit(ok==0?0:1);
        }
    }
    close(results[1]);
    for(int i=0;i<workers;i++)close(tasks[i][0]);
    int failed=0;
    for(int i=0;i<count;i++){
        struct task task={i,values[i]};
        if(transfer(tasks[i%workers][1],&task,sizeof task,1)<0)failed=1;
    }
    for(int i=0;i<workers;i++){struct task stop={-1,0};if(transfer(tasks[i][1],&stop,sizeof stop,1)<0)failed=1;close(tasks[i][1]);}
    struct result output[16];int seen[16]={0};
    for(int i=0;i<count;i++){
        struct result result;
        if(transfer(results[0],&result,sizeof result,0)<0){failed=1;break;}
        if(result.index<0||result.index>=count||seen[result.index])failed=1;
        else{output[result.index]=result;seen[result.index]=1;}
    }
    close(results[0]);
    for(int i=0;i<workers;i++){int status=0;if(waitpid(pids[i],&status,0)<0||!WIFEXITED(status)||WEXITSTATUS(status)!=0)failed=1;}
    for(int i=0;i<count;i++)if(!seen[i])failed=1;
    if(failed){fprintf(stderr,"worker farm failed\n");return 1;}
    for(int i=0;i<count;i++)printf("%d value=%lld square=%lld cube=%lld\n",i,output[i].value,output[i].square,output[i].cube);
    return 0;
}
