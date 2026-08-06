#define _POSIX_C_SOURCE 200809L
#include <dirent.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
struct item{char*name;off_t size;};
static char*join(const char*a,const char*b){size_t n=strlen(a),m=strlen(b);char*p=malloc(n+m+2);if(p)sprintf(p,"%s/%s",a,b);return p;}
static int cmp(const void*a,const void*b){return strcmp(((const struct item*)a)->name,((const struct item*)b)->name);}
static int fail(void){fputs("c1521_fs_024: error\n",stderr);return 1;}
int main(int argc,char**argv){if(argc!=3||argv[2][0]=='-'||argv[2][0]=='+')return fail();char*end=NULL;errno=0;unsigned long long min=strtoull(argv[2],&end,10);if(errno||end==argv[2]||*end)return fail();DIR*d=opendir(argv[1]);if(!d)return fail();struct item*v=NULL;size_t n=0,cap=0;int bad=0;struct dirent*e;while((e=readdir(d))){if(!strcmp(e->d_name,".")||!strcmp(e->d_name,".."))continue;char*p=join(argv[1],e->d_name);struct stat s;if(!p||lstat(p,&s)<0){free(p);bad=1;break;}free(p);if(S_ISREG(s.st_mode)&&(unsigned long long)s.st_size>=min){if(n==cap){size_t c=cap?cap*2:8;void*w=realloc(v,c*sizeof*v);if(!w){bad=1;break;}v=w;cap=c;}v[n].name=strdup(e->d_name);if(!v[n].name){bad=1;break;}v[n++].size=s.st_size;}}if(closedir(d)<0)bad=1;if(bad){for(size_t i=0;i<n;i++)free(v[i].name);free(v);return fail();}if(n>1)qsort(v,n,sizeof*v,cmp);for(size_t i=0;i<n;i++){printf("%s %lld\n",v[i].name,(long long)v[i].size);free(v[i].name);}free(v);return 0;}
