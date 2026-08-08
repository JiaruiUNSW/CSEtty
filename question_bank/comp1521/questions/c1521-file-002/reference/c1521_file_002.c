#define _POSIX_C_SOURCE 200809L
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
static long long solve(const unsigned char*a,size_t n){(void)a;(void)n;long long r=0;for(size_t i=0;i<n;i++)if(a[i]=='\n')r++;return r;}
int main(int argc,char**argv){if(argc!=2)return 1;int fd=open(argv[1],O_RDONLY);if(fd<0)return 1;size_t n=0,cap=256;unsigned char*a=malloc(cap);if(!a){close(fd);return 1;}for(;;){if(n==cap){cap*=2;void*p=realloc(a,cap);if(!p){free(a);close(fd);return 1;}a=p;}ssize_t got=read(fd,a+n,cap-n);if(got<0){free(a);close(fd);return 1;}if(got==0)break;n+=(size_t)got;}close(fd);printf("result: %lld\n",solve(a,n));free(a);return 0;}
