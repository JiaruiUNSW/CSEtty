#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

struct summary { long long even_sum,odd_sum,minimum,maximum; unsigned long long count,even,odd; int have,ok; };
struct shared { struct summary value; pthread_mutex_t mutex; };
struct job { const long long *values; size_t count,start; struct shared *shared; int failed; };

static int transfer(int fd,void *buffer,size_t size,int writing){
    unsigned char *p=buffer;while(size){ssize_t n=writing?write(fd,p,size):read(fd,p,size);if(n<0&&errno==EINTR)continue;if(n<=0)return -1;p+=(size_t)n;size-=(size_t)n;}return 0;
}
static void *analyse(void *opaque){
    struct job *job=opaque;struct summary local={.ok=1};
    for(size_t i=job->start;i<job->count;i+=3){
        long long value=job->values[i];local.count++;
        if(value%2==0){local.even++;local.even_sum+=value;}else{local.odd++;local.odd_sum+=value;}
        if(!local.have||value<local.minimum)local.minimum=value;
        if(!local.have||value>local.maximum)local.maximum=value;
        local.have=1;
    }
    if(pthread_mutex_lock(&job->shared->mutex)!=0){job->failed=1;return NULL;}
    struct summary *out=&job->shared->value;
    out->count+=local.count;out->even+=local.even;out->odd+=local.odd;out->even_sum+=local.even_sum;out->odd_sum+=local.odd_sum;
    if(local.have){if(!out->have||local.minimum<out->minimum)out->minimum=local.minimum;if(!out->have||local.maximum>out->maximum)out->maximum=local.maximum;out->have=1;}
    if(pthread_mutex_unlock(&job->shared->mutex)!=0)job->failed=1;
    return NULL;
}
static int child_work(const char *path,int output){
    FILE *input=fopen(path,"r");if(!input)return -1;
    long long *values=NULL;size_t count=0,capacity=0;int failed=0;
    for(;;){long long value;int result=fscanf(input,"%lld",&value);if(result==EOF)break;if(result!=1){failed=1;break;}
        if(count==capacity){size_t next=capacity?capacity*2:64;long long *grown=realloc(values,next*sizeof *grown);if(!grown){failed=1;break;}values=grown;capacity=next;}
        values[count++]=value;if(count>1000){failed=1;break;}
    }
    if(ferror(input)||fclose(input)!=0||count==0)failed=1;
    struct shared shared={.value={.ok=1},.mutex=PTHREAD_MUTEX_INITIALIZER};
    pthread_t threads[3];struct job jobs[3];int created=0;
    if(!failed)for(int i=0;i<3;i++){jobs[i]=(struct job){values,count,(size_t)i,&shared,0};if(pthread_create(&threads[i],NULL,analyse,&jobs[i])!=0)break;created++;}
    if(created!=3)failed=1;
    for(int i=0;i<created;i++)if(pthread_join(threads[i],NULL)!=0||jobs[i].failed)failed=1;
    if(pthread_mutex_destroy(&shared.mutex)!=0)failed=1;
    shared.value.ok=!failed&&shared.value.have;
    int sent=transfer(output,&shared.value,sizeof shared.value,1);
    free(values);return sent==0&&shared.value.ok?0:-1;
}
int main(int argc,char **argv){
    if(argc!=2){fprintf(stderr,"usage: %s FILE\n",argv[0]);return 1;}
    int channel[2];if(pipe(channel)<0)return 1;pid_t pid=fork();if(pid<0)return 1;
    if(pid==0){close(channel[0]);int ok=child_work(argv[1],channel[1]);close(channel[1]);_exit(ok==0?0:1);}
    close(channel[1]);struct summary result;int failed=transfer(channel[0],&result,sizeof result,0)<0||!result.ok;close(channel[0]);
    int status=0;if(waitpid(pid,&status,0)<0||!WIFEXITED(status)||WEXITSTATUS(status)!=0)failed=1;
    if(failed){fprintf(stderr,"analysis child failed\n");return 1;}
    printf("count=%llu even=%llu even_sum=%lld odd=%llu odd_sum=%lld min=%lld max=%lld\n",result.count,result.even,result.even_sum,result.odd,result.odd_sum,result.minimum,result.maximum);
    return 0;
}
