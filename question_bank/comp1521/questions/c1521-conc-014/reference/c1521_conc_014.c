#define _POSIX_C_SOURCE 200809L
#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

struct summary { uint64_t words, chars; uint32_t longest; int ok; };

static int transfer(int fd, void *buffer, size_t size, int writing) {
    unsigned char *p = buffer;
    while (size > 0) {
        ssize_t n = writing ? write(fd,p,size) : read(fd,p,size);
        if (n < 0 && errno == EINTR) continue;
        if (n <= 0) return -1;
        p += (size_t)n; size -= (size_t)n;
    }
    return 0;
}

static int produce(const char *path, int output) {
    int fd=open(path,O_RDONLY);
    if(fd<0)return -1;
    unsigned char buffer[4096];
    uint32_t length=0;
    for(;;){
        ssize_t n=read(fd,buffer,sizeof buffer);
        if(n<0&&errno==EINTR)continue;
        if(n<0){close(fd);return -1;}
        if(n==0)break;
        for(ssize_t i=0;i<n;i++){
            if(isspace(buffer[i])){
                if(length>0){if(transfer(output,&length,sizeof length,1)<0){close(fd);return -1;}length=0;}
            }else{
                if(length==UINT32_MAX){close(fd);return -1;}
                length++;
            }
        }
    }
    if(length>0&&transfer(output,&length,sizeof length,1)<0){close(fd);return -1;}
    uint32_t sentinel=0;
    int ok=transfer(output,&sentinel,sizeof sentinel,1);
    if(close(fd)<0)ok=-1;
    return ok;
}

static int aggregate(int input,int output){
    struct summary result={0,0,0,1};
    for(;;){
        uint32_t length;
        if(transfer(input,&length,sizeof length,0)<0){result.ok=0;break;}
        if(length==0)break;
        result.words++;
        result.chars+=length;
        if(length>result.longest)result.longest=length;
    }
    return transfer(output,&result,sizeof result,1)==0&&result.ok?0:-1;
}

int main(int argc,char **argv){
    if(argc!=2){fprintf(stderr,"usage: %s FILE\n",argv[0]);return 1;}
    int first[2],second[2];
    if(pipe(first)<0||pipe(second)<0)return 1;
    pid_t producer=fork();
    if(producer<0)return 1;
    if(producer==0){
        close(first[0]);close(second[0]);close(second[1]);
        int ok=produce(argv[1],first[1]);
        close(first[1]);_exit(ok==0?0:1);
    }
    pid_t aggregator=fork();
    if(aggregator<0)return 1;
    if(aggregator==0){
        close(first[1]);close(second[0]);
        int ok=aggregate(first[0],second[1]);
        close(first[0]);close(second[1]);_exit(ok==0?0:1);
    }
    close(first[0]);close(first[1]);close(second[1]);
    struct summary result;
    int failed=transfer(second[0],&result,sizeof result,0)<0||!result.ok;
    close(second[0]);
    int statuses[2]; pid_t pids[2]={producer,aggregator};
    for(int i=0;i<2;i++)if(waitpid(pids[i],&statuses[i],0)<0||!WIFEXITED(statuses[i])||WEXITSTATUS(statuses[i])!=0)failed=1;
    if(failed){fprintf(stderr,"pipeline failed\n");return 1;}
    printf("words=%llu chars=%llu longest=%u\n",(unsigned long long)result.words,(unsigned long long)result.chars,result.longest);
    return 0;
}
