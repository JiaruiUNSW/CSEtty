#include <stdint.h>
#include <stdio.h>
static uint32_t solve(uint32_t x,uint32_t y,unsigned k){(void)x;(void)y;(void)k;k&=31u;uint32_t mask=k?~0u<<k:~0u;return (x&mask)|(y&~mask);}
int main(void){unsigned x,y,k;if(scanf("%x%x%u",&x,&y,&k)!=3)return 1;printf("result: %08x\n",solve(x,y,k));return 0;}
