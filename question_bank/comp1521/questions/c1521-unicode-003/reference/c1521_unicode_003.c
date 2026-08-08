#include <stdint.h>
#include <stdio.h>
static long long solve(uint32_t cp){long long w;if(cp>0x10ffffu||(cp>=0xd800u&&cp<=0xdfffu))return -1;if(cp<=0x7fu)w=1;else if(cp<=0x7ffu)w=2;else if(cp<=0xffffu)w=3;else w=4;return w-1;}
int main(void){unsigned cp;if(scanf("%x",&cp)!=1)return 1;printf("result: %lld\n",solve(cp));return 0;}
