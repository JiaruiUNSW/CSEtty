#include <stdint.h>
#include <stdio.h>
static long long solve(uint32_t cp){if(cp>0x10ffffu||(cp>=0xd800u&&cp<=0xdfffu))return -1;if(cp<=0x7fu)return 1;if(cp<=0x7ffu)return 2;if(cp<=0xffffu)return 3;return 4;}
int main(void){unsigned cp;if(scanf("%x",&cp)!=1)return 1;printf("result: %lld\n",solve(cp));return 0;}
