#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>
static int fail(void){fputs("c1521_fs_020: error\n",stderr);return 1;}
int main(int argc,char**argv){if(argc!=3||argv[2][0]=='-'||argv[2][0]=='+')return fail();char*end=NULL;errno=0;unsigned long long index=strtoull(argv[2],&end,10);if(errno||end==argv[2]||*end)return fail();int fd=open(argv[1],O_RDONLY);if(fd<0)return fail();struct stat st;if(fstat(fd,&st)<0||!S_ISREG(st.st_mode)||st.st_size<0||st.st_size%6){close(fd);return fail();}unsigned long long count=(unsigned long long)st.st_size/6;if(index>=count){if(close(fd)<0)return fail();puts("NOT FOUND");return 0;}if(index>(unsigned long long)LLONG_MAX/6){close(fd);return fail();}unsigned char r[6];ssize_t n=pread(fd,r,6,(off_t)(index*6));if(n!=6||r[5]!='\n'||close(fd)<0)return fail();if(fwrite(r,1,5,stdout)!=5)return fail();putchar('\n');return 0;}
