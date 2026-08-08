#include <stdint.h>
#include <stdio.h>
static long long solve(uint32_t cp){if(cp>0x10ffffu||(cp>=0xd800u&&cp<=0xdfffu))return -1;if(cp<=0x7fu)return cp;if(cp<=0x7ffu)return (0xc0u|(cp>>6))+(0x80u|(cp&63u));if(cp<=0xffffu)return (0xe0u|(cp>>12))+(0x80u|((cp>>6)&63u))+(0x80u|(cp&63u));return (0xf0u|(cp>>18))+(0x80u|((cp>>12)&63u))+(0x80u|((cp>>6)&63u))+(0x80u|(cp&63u));}
int main(void){unsigned cp;if(scanf("%x",&cp)!=1)return 1;printf("result: %lld\n",solve(cp));return 0;}
