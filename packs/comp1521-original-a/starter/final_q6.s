.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    li   $t1, 0
    # TODO: inspect all 32 bits and place the count in $t1.
    move $a0, $t1
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall

