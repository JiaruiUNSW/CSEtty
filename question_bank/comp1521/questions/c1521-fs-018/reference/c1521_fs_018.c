#define _POSIX_C_SOURCE 200809L
#include <dirent.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
struct group{char*ext;uint64_t count,bytes;};
static char*join(const char*a,const char*b){size_t n=strlen(a),m=strlen(b);char*p=malloc(n+m+2);if(p)sprintf(p,"%s/%s",a,b);return p;}
static int cmp(const void*a,const void*b){return strcmp(((const struct group*)a)->ext,((const struct group*)b)->ext);}
static int fail(void){fputs("c1521_fs_018: error\n",stderr);return 1;}
int main(int argc,char**argv){if(argc!=2)return fail();DIR*d=opendir(argv[1]);if(!d)return fail();struct group*g=NULL;size_t n=0,cap=0;int bad=0;struct dirent*e;while((e=readdir(d))){if(!strcmp(e->d_name,".")||!strcmp(e->d_name,".."))continue;char*p=join(argv[1],e->d_name);struct stat s;if(!p||lstat(p,&s)<0){free(p);bad=1;break;}free(p);if(!S_ISREG(s.st_mode))continue;char*dot=strrchr(e->d_name,'.');const char*ext=(dot&&dot!=e->d_name&&dot[1])?dot+1:"[none]";size_t i=0;while(i<n&&strcmp(g[i].ext,ext))i++;if(i==n){if(n==cap){size_t c=cap?cap*2:8;void*v=realloc(g,c*sizeof*g);if(!v){bad=1;break;}g=v;cap=c;}g[n].ext=strdup(ext);if(!g[n].ext){bad=1;break;}g[n].count=g[n].bytes=0;i=n++;}g[i].count++;g[i].bytes+=(uint64_t)s.st_size;}if(closedir(d)<0)bad=1;if(bad){for(size_t i=0;i<n;i++)free(g[i].ext);free(g);return fail();}if(n>1)qsort(g,n,sizeof*g,cmp);for(size_t i=0;i<n;i++){printf("%s %llu %llu\n",g[i].ext,(unsigned long long)g[i].count,(unsigned long long)g[i].bytes);free(g[i].ext);}free(g);return 0;}
