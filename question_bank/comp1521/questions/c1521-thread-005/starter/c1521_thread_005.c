#include <pthread.h>
#include <stdio.h>
#define MODE 4
static int values[100],n;static long long total;static pthread_mutex_t lock=PTHREAD_MUTEX_INITIALIZER;
struct job{int start;};
static void*worker(void*arg){(void)arg;(void)lock;return NULL;}
int main(void){if(scanf("%d",&n)!=1||n<0||n>100)return 1;for(int i=0;i<n;i++)if(scanf("%d",&values[i])!=1)return 1;pthread_t t[3];struct job j[3];for(int i=0;i<3;i++){j[i].start=i;if(pthread_create(&t[i],NULL,worker,&j[i])!=0)return 1;}for(int i=0;i<3;i++)if(pthread_join(t[i],NULL)!=0)return 1;pthread_mutex_destroy(&lock);printf("result: %lld\n",total);return 0;}
