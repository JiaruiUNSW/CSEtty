#define _POSIX_C_SOURCE 200809L
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
static char*join(const char*a,const char*b){size_t n=strlen(a),m=strlen(b);char*p=malloc(n+m+2);if(p)sprintf(p,"%s/%s",a,b);return p;}
static int fail(void){fputs("c1521_fs_016: error\n",stderr);return 1;}
int main(int argc,char**argv){if(argc!=2)return fail();DIR*d=opendir(argv[1]);if(!d)return fail();char*best=NULL;off_t size=0;int bad=0;struct dirent*e;while((e=readdir(d))){if(!strcmp(e->d_name,".")||!strcmp(e->d_name,".."))continue;char*p=join(argv[1],e->d_name);struct stat s;if(!p||lstat(p,&s)<0){free(p);bad=1;break;}free(p);if(S_ISREG(s.st_mode)&&(!best||s.st_size>size||(s.st_size==size&&strcmp(e->d_name,best)<0))){char*n=strdup(e->d_name);if(!n){bad=1;break;}free(best);best=n;size=s.st_size;}}if(closedir(d)<0)bad=1;if(bad){free(best);return fail();}if(best)printf("%s %lld\n",best,(long long)size);else puts("NONE");free(best);return 0;}
