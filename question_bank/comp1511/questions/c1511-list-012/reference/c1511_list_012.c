#include <stdio.h>
#include <stdlib.h>
struct node{int value;struct node*next;};
static long long solve(const struct node*h){if(!h)return 0;int first=h->value,last=first;for(;h;h=h->next)last=h->value;long long d=(long long)first-last;return d<0?-d:d;}
int main(int argc,char**argv){
    struct node*head=NULL;struct node**tail=&head;
    for(int i=1;i<argc;i++){struct node*n=malloc(sizeof*n);if(!n)return 1;n->value=atoi(argv[i]);n->next=NULL;*tail=n;tail=&n->next;}
    printf("result: %lld\n",solve(head));
    while(head){struct node*next=head->next;free(head);head=next;}
    return 0;
}
