#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
static int fail(void){fputs("c1521_fs_023: error\n",stderr);return 1;}
static int num(const char*s,unsigned long long*v){if(*s=='-'||*s=='+')return 0;char*e=NULL;errno=0;*v=strtoull(s,&e,10);return !errno&&e!=s&&!*e;}
int main(int argc,char**argv){unsigned long long off,len;if(argc!=5||!strcmp(argv[1],argv[2])||!num(argv[3],&off)||!num(argv[4],&len)||off>(unsigned long long)LLONG_MAX)return fail();int in=open(argv[1],O_RDONLY);if(in<0)return fail();int out=open(argv[2],O_WRONLY|O_CREAT|O_TRUNC,0600);if(out<0){close(in);return fail();}unsigned char buf[4096];unsigned long long copied=0;int bad=0;while(copied<len){size_t want=len-copied<sizeof buf?(size_t)(len-copied):sizeof buf;if(off>ULLONG_MAX-copied||off+copied>(unsigned long long)LLONG_MAX){bad=1;break;}ssize_t n=pread(in,buf,want,(off_t)(off+copied));if(n<0&&errno==EINTR)continue;if(n<0){bad=1;break;}if(!n)break;size_t done=0;while(done<(size_t)n){ssize_t w=write(out,buf+done,(size_t)n-done);if(w<0&&errno==EINTR)continue;if(w<=0){bad=1;break;}done+=(size_t)w;}if(bad)break;copied+=(unsigned long long)n;}if(close(in)<0||close(out)<0)bad=1;if(bad)return fail();printf("%llu\n",copied);return 0;}
