#define _POSIX_C_SOURCE 200809L
#include <dirent.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
struct totals{uint64_t files,bytes;unsigned depth;};
static char*join(const char*a,const char*b){size_t n=strlen(a),m=strlen(b);char*p=malloc(n+m+2);if(p)sprintf(p,"%s/%s",a,b);return p;}
static int walk(const char*p,unsigned depth,struct totals*t){DIR*d=opendir(p);if(!d)return -1;int bad=0;struct dirent*e;while((e=readdir(d))){if(!strcmp(e->d_name,".")||!strcmp(e->d_name,".."))continue;char*q=join(p,e->d_name);struct stat s;if(!q||lstat(q,&s)<0){free(q);bad=1;break;}if(S_ISDIR(s.st_mode))bad=walk(q,depth+1,t)<0;else if(S_ISREG(s.st_mode)){t->files++;t->bytes+=(uint64_t)s.st_size;if(depth>t->depth)t->depth=depth;}free(q);if(bad)break;}if(closedir(d)<0)bad=1;return bad?-1:0;}
int main(int argc,char**argv){if(argc!=2){fputs("c1521_fs_019: error\n",stderr);return 1;}struct totals t={0};if(walk(argv[1],0,&t)<0){fputs("c1521_fs_019: error\n",stderr);return 1;}printf("files=%llu bytes=%llu max_depth=%u\n",(unsigned long long)t.files,(unsigned long long)t.bytes,t.depth);return 0;}
