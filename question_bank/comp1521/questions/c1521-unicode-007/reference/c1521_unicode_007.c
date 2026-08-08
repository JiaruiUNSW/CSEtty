#include <stdint.h>
#include <stdio.h>
static long long solve(uint32_t cp){if(cp>0x10ffffu||(cp>=0xd800u&&cp<=0xdfffu))return -1;return cp>>16;}
int main(void){unsigned cp;if(scanf("%x",&cp)!=1)return 1;printf("result: %lld\n",solve(cp));return 0;}
