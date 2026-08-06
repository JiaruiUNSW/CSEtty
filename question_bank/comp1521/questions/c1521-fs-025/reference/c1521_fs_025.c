#define _POSIX_C_SOURCE 200809L
#include <dirent.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
struct item{char*path;uint64_t bytes;};struct list{struct item*v;size_t n,cap;};
static char*join(const char*a,const char*b){size_t n=strlen(a),m=strlen(b);char*p=malloc(n+m+2);if(p)sprintf(p,"%s/%s",a,b);return p;}
static int add(struct list*l,const char*p,size_t*index){if(l->n==l->cap){size_t c=l->cap?l->cap*2:8;void*v=realloc(l->v,c*sizeof*l->v);if(!v)return -1;l->v=v;l->cap=c;}l->v[l->n].path=strdup(p);if(!l->v[l->n].path)return -1;l->v[l->n].bytes=0;*index=l->n++;return 0;}
static int walk(const char*full,const char*rel,struct list*l){size_t me;if(add(l,rel[0]?rel:".",&me)<0)return -1;DIR*d=opendir(full);if(!d)return -1;int bad=0;struct dirent*e;while((e=readdir(d))){if(!strcmp(e->d_name,".")||!strcmp(e->d_name,".."))continue;char*f=join(full,e->d_name);char*r=rel[0]?join(rel,e->d_name):strdup(e->d_name);struct stat s;if(!f||!r||lstat(f,&s)<0){free(f);free(r);bad=1;break;}if(S_ISREG(s.st_mode))l->v[me].bytes+=(uint64_t)s.st_size;else if(S_ISDIR(s.st_mode))bad=walk(f,r,l)<0;free(f);free(r);if(bad)break;}if(closedir(d)<0)bad=1;return bad?-1:0;}
static int cmp(const void*a,const void*b){return strcmp(((const struct item*)a)->path,((const struct item*)b)->path);}
int main(int argc,char**argv){if(argc!=2){fputs("c1521_fs_025: error\n",stderr);return 1;}struct list l={0};if(walk(argv[1],"",&l)<0){for(size_t i=0;i<l.n;i++)free(l.v[i].path);free(l.v);fputs("c1521_fs_025: error\n",stderr);return 1;}qsort(l.v,l.n,sizeof*l.v,cmp);for(size_t i=0;i<l.n;i++){printf("%s %llu\n",l.v[i].path,(unsigned long long)l.v[i].bytes);free(l.v[i].path);}free(l.v);return 0;}
