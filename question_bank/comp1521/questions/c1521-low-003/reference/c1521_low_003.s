.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    li   $t1, 1
    move $t2, $zero
sum_loop:
    slt  $t3, $t0, $t1
    bne  $t3, $zero, sum_done
    addu $t2, $t2, $t1
    addiu $t1, $t1, 1
    b    sum_loop
sum_done:
    move $a0, $t2
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
