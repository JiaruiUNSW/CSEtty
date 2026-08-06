#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

struct task { int index; long long value; };
struct shared {
    struct task queue[8]; int head,tail,count,capacity,done,failed;
    int task_count; long long *values,*results;
    pthread_mutex_t mutex; pthread_cond_t not_empty,not_full;
};

static void fail_locked(struct shared *shared){
    shared->failed=1;shared->done=1;
    pthread_cond_broadcast(&shared->not_empty);
    pthread_cond_broadcast(&shared->not_full);
}

static void *produce(void *opaque){
    struct shared *shared=opaque;
    for(int i=0;i<shared->task_count;i++){
        if(pthread_mutex_lock(&shared->mutex)!=0)return NULL;
        while(shared->count==shared->capacity&&!shared->failed){
            if(pthread_cond_wait(&shared->not_full,&shared->mutex)!=0){fail_locked(shared);break;}
        }
        if(shared->failed){pthread_mutex_unlock(&shared->mutex);return NULL;}
        shared->queue[shared->tail]=(struct task){i,shared->values[i]};
        shared->tail=(shared->tail+1)%shared->capacity;shared->count++;
        if(pthread_cond_signal(&shared->not_empty)!=0)fail_locked(shared);
        pthread_mutex_unlock(&shared->mutex);
    }
    if(pthread_mutex_lock(&shared->mutex)==0){
        shared->done=1;
        if(pthread_cond_broadcast(&shared->not_empty)!=0)shared->failed=1;
        pthread_mutex_unlock(&shared->mutex);
    }
    return NULL;
}

static void *consume(void *opaque){
    struct shared *shared=opaque;
    for(;;){
        if(pthread_mutex_lock(&shared->mutex)!=0)return NULL;
        while(shared->count==0&&!shared->done&&!shared->failed){
            if(pthread_cond_wait(&shared->not_empty,&shared->mutex)!=0){fail_locked(shared);break;}
        }
        if(shared->count==0&&(shared->done||shared->failed)){pthread_mutex_unlock(&shared->mutex);return NULL;}
        struct task task=shared->queue[shared->head];
        shared->head=(shared->head+1)%shared->capacity;shared->count--;
        if(pthread_cond_signal(&shared->not_full)!=0)fail_locked(shared);
        pthread_mutex_unlock(&shared->mutex);
        shared->results[task.index]=task.value*task.value;
    }
}

int main(int argc,char **argv){
    if(argc<4||argc>19){fprintf(stderr,"usage: %s CAPACITY CONSUMERS VALUE [VALUE ...]\n",argv[0]);return 1;}
    char *end_c=NULL,*end_n=NULL;
    long capacity=strtol(argv[1],&end_c,10),consumers=strtol(argv[2],&end_n,10);
    if(*argv[1]=='\0'||*end_c!='\0'||capacity<1||capacity>8||*argv[2]=='\0'||*end_n!='\0'||consumers<1||consumers>4)return 1;
    int task_count=argc-3;long long values[16],results[16]={0};
    for(int i=0;i<task_count;i++){
        char *end=NULL;long value=strtol(argv[i+3],&end,10);
        if(*argv[i+3]=='\0'||*end!='\0'||value<-10000||value>10000)return 1;
        values[i]=value;
    }
    struct shared shared={.capacity=(int)capacity,.task_count=task_count,.values=values,.results=results,
        .mutex=PTHREAD_MUTEX_INITIALIZER,.not_empty=PTHREAD_COND_INITIALIZER,.not_full=PTHREAD_COND_INITIALIZER};
    pthread_t producer,consumer_ids[4];
    int producer_created=pthread_create(&producer,NULL,produce,&shared)==0;
    int created=0;
    if(producer_created)for(;created<consumers;created++)if(pthread_create(&consumer_ids[created],NULL,consume,&shared)!=0)break;
    if(!producer_created||created!=consumers){
        if(pthread_mutex_lock(&shared.mutex)==0){fail_locked(&shared);pthread_mutex_unlock(&shared.mutex);}
    }
    if(producer_created&&pthread_join(producer,NULL)!=0)shared.failed=1;
    for(int i=0;i<created;i++)if(pthread_join(consumer_ids[i],NULL)!=0)shared.failed=1;
    int failed=shared.failed||!producer_created||created!=consumers;
    if(!failed){
        long long total=0;
        for(int i=0;i<task_count;i++){printf("%d square=%lld\n",i,results[i]);total+=results[i];}
        printf("total=%lld\n",total);
    }
    if(pthread_cond_destroy(&shared.not_empty)!=0||pthread_cond_destroy(&shared.not_full)!=0||pthread_mutex_destroy(&shared.mutex)!=0)failed=1;
    return failed?1:0;
}
