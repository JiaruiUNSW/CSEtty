.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    li   $t1, 0
    li   $t2, 32
bit_loop:
    andi $t3, $t0, 1
    add  $t1, $t1, $t3
    srl  $t0, $t0, 1
    addi $t2, $t2, -1
    bnez $t2, bit_loop
    move $a0, $t1
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall

