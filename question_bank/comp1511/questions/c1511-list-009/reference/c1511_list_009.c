#include <stdio.h>
#include <stdlib.h>
struct node{int value;struct node*next;};
static long long solve(const struct node*h){int a[100],n=0;for(;h&&n<100;h=h->next)a[n++]=h->value;for(int i=0;i<n/2;i++)if(a[i]!=a[n-1-i])return 0;return 1;}
int main(int argc,char**argv){
    struct node*head=NULL;struct node**tail=&head;
    for(int i=1;i<argc;i++){struct node*n=malloc(sizeof*n);if(!n)return 1;n->value=atoi(argv[i]);n->next=NULL;*tail=n;tail=&n->next;}
    printf("result: %lld\n",solve(head));
    while(head){struct node*next=head->next;free(head);head=next;}
    return 0;
}
