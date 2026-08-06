#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int hd(char c){if(c>='0'&&c<='9')return c-'0';if(c>='a'&&c<='f')return c-'a'+10;if(c>='A'&&c<='F')return c-'A'+10;return -1;}
int main(int argc,char**argv){if(argc!=2||strlen(argv[1])%2){fputs("c1521_fs_022: error\n",stderr);return 1;}size_t n=strlen(argv[1])/2;unsigned char*b=malloc(n?n:1);if(!b){fputs("c1521_fs_022: error\n",stderr);return 1;}for(size_t i=0;i<n;i++){int h=hd(argv[1][2*i]),l=hd(argv[1][2*i+1]);if(h<0||l<0){free(b);fputs("c1521_fs_022: error\n",stderr);return 1;}b[i]=h*16+l;}for(size_t at=0;at<n;){size_t start=at;if(n-at<2||n-at-2<b[at+1]){printf("invalid %zu\n",start);free(b);return 0;}at+=2+b[at+1];}for(size_t at=0;at<n;){unsigned type=b[at],len=b[at+1],sum=0;for(unsigned i=0;i<len;i++)sum=(sum+b[at+2+i])&255;printf("%u %u %u\n",type,len,sum);at+=2+len;}free(b);return 0;}
