#include <stdio.h>
#include <stdlib.h>
struct node{int value;struct node*next;};
static long long solve(const struct node*h){(void)h;return 0;}
int main(int argc,char**argv){
    struct node*head=NULL;struct node**tail=&head;
    for(int i=1;i<argc;i++){struct node*n=malloc(sizeof*n);if(!n)return 1;n->value=atoi(argv[i]);n->next=NULL;*tail=n;tail=&n->next;}
    printf("result: %lld\n",solve(head));
    while(head){struct node*next=head->next;free(head);head=next;}
    return 0;
}
