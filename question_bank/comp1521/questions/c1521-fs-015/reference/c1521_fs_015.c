#define _POSIX_C_SOURCE 200809L
#include <dirent.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
static char*join(const char*a,const char*b){size_t n=strlen(a),m=strlen(b);char*p=malloc(n+m+2);if(p)sprintf(p,"%s/%s",a,b);return p;}
static int ends(const char*n,const char*s){size_t a=strlen(n),b=strlen(s);return a>=b&&!memcmp(n+a-b,s,b);}
static int walk(const char*path,const char*suffix,uint64_t*count,uint64_t*bytes){DIR*d=opendir(path);if(!d)return -1;struct dirent*e;int bad=0;while((e=readdir(d))){if(!strcmp(e->d_name,".")||!strcmp(e->d_name,".."))continue;char*p=join(path,e->d_name);struct stat st;if(!p||lstat(p,&st)<0){free(p);bad=1;break;}if(S_ISDIR(st.st_mode)){if(walk(p,suffix,count,bytes)<0)bad=1;}else if(S_ISREG(st.st_mode)&&ends(e->d_name,suffix)){(*count)++;*bytes+=(uint64_t)st.st_size;}free(p);if(bad)break;}if(closedir(d)<0)bad=1;return bad?-1:0;}
int main(int argc,char**argv){if(argc!=3||!argv[2][0]){fputs("c1521_fs_015: error\n",stderr);return 1;}uint64_t n=0,b=0;if(walk(argv[1],argv[2],&n,&b)<0){fputs("c1521_fs_015: error\n",stderr);return 1;}printf("files=%llu bytes=%llu\n",(unsigned long long)n,(unsigned long long)b);return 0;}
