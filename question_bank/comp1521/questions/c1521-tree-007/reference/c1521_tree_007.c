#define _POSIX_C_SOURCE 200809L
#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
struct summary{long long files,bytes,depth,text,dirs,largest,sources;};
static int walk(const char*path,int depth,struct summary*s){DIR*d=opendir(path);if(!d)return -1;s->dirs++;struct dirent*e;while((e=readdir(d))){if(strcmp(e->d_name,".")==0||strcmp(e->d_name,"..")==0||strcmp(e->d_name,".keep")==0)continue;char child[1024];if(snprintf(child,sizeof child,"%s/%s",path,e->d_name)>=(int)sizeof child){closedir(d);return -1;}struct stat st;if(lstat(child,&st)!=0){closedir(d);return -1;}if(S_ISDIR(st.st_mode)){if(walk(child,depth+1,s)!=0){closedir(d);return -1;}}else if(S_ISREG(st.st_mode)){s->files++;s->bytes+=st.st_size;if(depth>s->depth)s->depth=depth;if(st.st_size>s->largest)s->largest=st.st_size;size_t n=strlen(e->d_name);if(n>=4&&strcmp(e->d_name+n-4,".txt")==0)s->text++;if(n>=2&&strcmp(e->d_name+n-2,".c")==0)s->sources++;}}closedir(d);return 0;}
int main(int argc,char**argv){if(argc!=2)return 1;struct summary s={0};if(walk(argv[1],0,&s)!=0)return 1;printf("result: %lld\n",(long long)(s.sources));return 0;}
