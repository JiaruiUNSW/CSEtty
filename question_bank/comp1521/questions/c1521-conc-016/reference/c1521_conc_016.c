#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

struct shared { unsigned long long counts[256]; pthread_mutex_t mutex; };
struct job { const unsigned char *data; size_t start,end; struct shared *shared; int failed; };

static void *count_slice(void *opaque){
    struct job *job=opaque;
    unsigned long long local[256]={0};
    for(size_t i=job->start;i<job->end;i++)local[job->data[i]]++;
    if(pthread_mutex_lock(&job->shared->mutex)!=0){job->failed=1;return NULL;}
    for(int i=0;i<256;i++)job->shared->counts[i]+=local[i];
    if(pthread_mutex_unlock(&job->shared->mutex)!=0)job->failed=1;
    return NULL;
}

int main(int argc,char **argv){
    if(argc!=3){fprintf(stderr,"usage: %s FILE THREADS\n",argv[0]);return 1;}
    char *end=NULL;long parsed=strtol(argv[2],&end,10);
    if(*argv[2]=='\0'||*end!='\0'||parsed<1||parsed>8)return 1;
    int fd=open(argv[1],O_RDONLY);if(fd<0)return 1;
    struct stat metadata;
    if(fstat(fd,&metadata)<0||!S_ISREG(metadata.st_mode)||metadata.st_size<0){close(fd);return 1;}
    size_t size=(size_t)metadata.st_size;
    unsigned char *data=malloc(size==0?1:size);if(data==NULL){close(fd);return 1;}
    size_t used=0;
    while(used<size){
        ssize_t n=read(fd,data+used,size-used);
        if(n<0&&errno==EINTR)continue;
        if(n<=0){free(data);close(fd);return 1;}
        used+=(size_t)n;
    }
    if(close(fd)<0){free(data);return 1;}
    int threads=(int)parsed;pthread_t ids[8];struct job jobs[8];
    struct shared shared={{0},PTHREAD_MUTEX_INITIALIZER};
    int created=0;
    for(int i=0;i<threads;i++){
        jobs[i]=(struct job){data,size*(size_t)i/(size_t)threads,size*(size_t)(i+1)/(size_t)threads,&shared,0};
        if(pthread_create(&ids[i],NULL,count_slice,&jobs[i])!=0)break;
        created++;
    }
    int failed=created!=threads;
    for(int i=0;i<created;i++)if(pthread_join(ids[i],NULL)!=0||jobs[i].failed)failed=1;
    unsigned long long total=0;
    if(!failed)for(int i=0;i<256;i++){if(shared.counts[i])printf("%02X=%llu\n",i,shared.counts[i]);total+=shared.counts[i];}
    if(!failed)printf("total=%llu\n",total);
    if(pthread_mutex_destroy(&shared.mutex)!=0)failed=1;
    free(data);return failed?1:0;
}
