.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    li   $v0, 5
    syscall
    move $t1, $v0
    beq  $t1, $zero, rotate_mask
    sllv $t2, $t0, $t1
    li   $t3, 8
    subu $t3, $t3, $t1
    srlv $t4, $t0, $t3
    or   $t0, $t2, $t4
rotate_mask:
    andi $t0, $t0, 255
    move $a0, $t0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
