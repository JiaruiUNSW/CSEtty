#include <stdint.h>
#include <stdio.h>
static uint32_t solve(uint32_t x,uint32_t y,unsigned k){(void)x;(void)y;(void)k;uint32_t e=(x>>23)&0xffu,f=x&0x7fffffu;if(e==0)return f?1u:0u;if(e==0xffu)return f?4u:3u;return 2u;}
int main(void){unsigned x,y,k;if(scanf("%x%x%u",&x,&y,&k)!=3)return 1;printf("result: %08x\n",solve(x,y,k));return 0;}
