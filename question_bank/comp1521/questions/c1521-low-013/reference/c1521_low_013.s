.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    li   $v0, 5
    syscall
    move $t1, $v0
    move $t2, $zero
    move $t3, $zero
threshold_loop:
    slt  $t4, $t2, $t0
    beq  $t4, $zero, threshold_done
    li   $v0, 5
    syscall
    slt  $t5, $t1, $v0
    addu $t3, $t3, $t5
    addiu $t2, $t2, 1
    b    threshold_loop
threshold_done:
    move $a0, $t3
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
