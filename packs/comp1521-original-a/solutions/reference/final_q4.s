.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    li   $t1, 0
    li   $t2, 1
sum_loop:
    bgt  $t2, $t0, sum_done
    add  $t1, $t1, $t2
    addi $t2, $t2, 1
    b    sum_loop
sum_done:
    move $a0, $t1
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall

