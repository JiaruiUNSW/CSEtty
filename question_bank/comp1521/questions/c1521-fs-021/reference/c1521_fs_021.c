#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>
static int fail(void){fputs("c1521_fs_021: error\n",stderr);return 1;}
static int num(const char*s,unsigned long long*v){if(*s=='-'||*s=='+')return 0;char*e=NULL;errno=0;*v=strtoull(s,&e,10);return !errno&&e!=s&&!*e;}
static int put4(int fd,const unsigned char*b,off_t off){size_t n=0;while(n<4){ssize_t w=pwrite(fd,b+n,4-n,off+(off_t)n);if(w<0&&errno==EINTR)continue;if(w<=0)return -1;n+=(size_t)w;}return 0;}
int main(int argc,char**argv){unsigned long long a,b;if(argc!=4||!num(argv[2],&a)||!num(argv[3],&b)||a>(unsigned long long)LLONG_MAX/4||b>(unsigned long long)LLONG_MAX/4)return fail();int fd=open(argv[1],O_RDWR);if(fd<0)return fail();struct stat st;if(fstat(fd,&st)<0||!S_ISREG(st.st_mode)||st.st_size<0||st.st_size%4){close(fd);return fail();}unsigned long long count=(unsigned long long)st.st_size/4;if(a>=count||b>=count){close(fd);return fail();}unsigned char x[4],y[4];if(pread(fd,x,4,(off_t)(a*4))!=4||pread(fd,y,4,(off_t)(b*4))!=4||put4(fd,y,(off_t)(a*4))<0||put4(fd,x,(off_t)(b*4))<0||lseek(fd,0,SEEK_SET)<0){close(fd);return fail();}unsigned char buf[1024];for(;;){ssize_t n=read(fd,buf,sizeof buf);if(n<0&&errno==EINTR)continue;if(n<0){close(fd);return fail();}if(!n)break;for(ssize_t i=0;i<n;i++)printf("%02x",buf[i]);}if(close(fd)<0)return fail();putchar('\n');return 0;}
