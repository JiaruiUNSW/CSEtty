.text
.globl main
main:
    # TODO: read exactly five signed integers and print the greatest.
    li   $a0, 0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall

