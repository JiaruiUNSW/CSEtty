#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>

struct shared { unsigned long long counts[21],total; pthread_mutex_t mutex; };
struct job { const char *path; struct shared *shared; int failed; };

static void *scan_file(void *opaque){
    struct job *job=opaque;unsigned long long local[21]={0},total=0;
    FILE *input=fopen(job->path,"r");if(input==NULL){job->failed=1;return NULL;}
    for(;;){
        int value;int result=fscanf(input,"%d",&value);
        if(result==EOF)break;
        if(result!=1||value<-10||value>10){job->failed=1;break;}
        local[value+10]++;total++;
    }
    if(ferror(input)||fclose(input)!=0)job->failed=1;
    if(job->failed)return NULL;
    if(pthread_mutex_lock(&job->shared->mutex)!=0){job->failed=1;return NULL;}
    for(int i=0;i<21;i++)job->shared->counts[i]+=local[i];
    job->shared->total+=total;
    if(pthread_mutex_unlock(&job->shared->mutex)!=0)job->failed=1;
    return NULL;
}

int main(int argc,char **argv){
    if(argc<2||argc>7){fprintf(stderr,"usage: %s FILE [FILE ...]\n",argv[0]);return 1;}
    int count=argc-1;struct shared shared={{0},0,PTHREAD_MUTEX_INITIALIZER};
    pthread_t threads[6];struct job jobs[6];int created=0;
    for(int i=0;i<count;i++){jobs[i]=(struct job){argv[i+1],&shared,0};if(pthread_create(&threads[i],NULL,scan_file,&jobs[i])!=0)break;created++;}
    int failed=created!=count;
    for(int i=0;i<created;i++)if(pthread_join(threads[i],NULL)!=0||jobs[i].failed)failed=1;
    if(!failed){
        for(int i=0;i<21;i++)if(shared.counts[i])printf("%d=%llu\n",i-10,shared.counts[i]);
        printf("values=%llu\n",shared.total);
    }
    if(pthread_mutex_destroy(&shared.mutex)!=0)failed=1;
    return failed?1:0;
}
