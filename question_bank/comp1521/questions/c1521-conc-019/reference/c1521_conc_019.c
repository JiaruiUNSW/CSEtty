#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

struct run { uint64_t count; unsigned char byte; };

static int write_all(int fd,const void *buffer,size_t size){
    const unsigned char *p=buffer;
    while(size){ssize_t n=write(fd,p,size);if(n<0&&errno==EINTR)continue;if(n<=0)return -1;p+=(size_t)n;size-=(size_t)n;}
    return 0;
}
static int read_record(int fd,struct run *run){
    unsigned char *p=(unsigned char *)run;size_t left=sizeof *run;
    while(left){ssize_t n=read(fd,p,left);if(n<0&&errno==EINTR)continue;if(n<0)return -1;if(n==0)return left==sizeof *run?0:-1;p+=(size_t)n;left-=(size_t)n;}
    return 1;
}
static int copy_file(const char *path,int output){
    int fd=open(path,O_RDONLY);if(fd<0)return -1;unsigned char buffer[4096];
    for(;;){ssize_t n=read(fd,buffer,sizeof buffer);if(n<0&&errno==EINTR)continue;if(n<0){close(fd);return -1;}if(n==0)break;if(write_all(output,buffer,(size_t)n)<0){close(fd);return -1;}}
    return close(fd);
}
static int encode(int input,int output){
    int have=0;unsigned char current=0,buffer[4096];uint64_t count=0;
    for(;;){ssize_t n=read(input,buffer,sizeof buffer);if(n<0&&errno==EINTR)continue;if(n<0)return -1;if(n==0)break;
        for(ssize_t i=0;i<n;i++){if(!have){current=buffer[i];count=1;have=1;}else if(buffer[i]==current){count++;}else{struct run run={count,current};if(write_all(output,&run,sizeof run)<0)return -1;current=buffer[i];count=1;}}
    }
    if(have){struct run run={count,current};if(write_all(output,&run,sizeof run)<0)return -1;}
    return 0;
}
int main(int argc,char **argv){
    if(argc!=2){fprintf(stderr,"usage: %s FILE\n",argv[0]);return 1;}
    int raw[2],encoded[2];if(pipe(raw)<0||pipe(encoded)<0)return 1;
    pid_t reader=fork();if(reader<0)return 1;
    if(reader==0){close(raw[0]);close(encoded[0]);close(encoded[1]);int ok=copy_file(argv[1],raw[1]);close(raw[1]);_exit(ok==0?0:1);}
    pid_t encoder=fork();if(encoder<0)return 1;
    if(encoder==0){close(raw[1]);close(encoded[0]);int ok=encode(raw[0],encoded[1]);close(raw[0]);close(encoded[1]);_exit(ok==0?0:1);}
    close(raw[0]);close(raw[1]);close(encoded[1]);
    struct run *runs=NULL;size_t count=0,capacity=0;uint64_t bytes=0;int failed=0;
    for(;;){struct run run;int result=read_record(encoded[0],&run);if(result==0)break;if(result<0){failed=1;break;}
        if(count==capacity){size_t next=capacity?capacity*2:16;struct run *grown=realloc(runs,next*sizeof *grown);if(!grown){failed=1;break;}runs=grown;capacity=next;}
        runs[count++]=run;bytes+=run.count;
    }
    close(encoded[0]);pid_t pids[2]={reader,encoder};
    for(int i=0;i<2;i++){int status=0;if(waitpid(pids[i],&status,0)<0||!WIFEXITED(status)||WEXITSTATUS(status)!=0)failed=1;}
    if(failed){free(runs);fprintf(stderr,"run pipeline failed\n");return 1;}
    for(size_t i=0;i<count;i++)printf("%02X %llu\n",runs[i].byte,(unsigned long long)runs[i].count);
    printf("runs=%zu bytes=%llu\n",count,(unsigned long long)bytes);free(runs);return 0;
}
