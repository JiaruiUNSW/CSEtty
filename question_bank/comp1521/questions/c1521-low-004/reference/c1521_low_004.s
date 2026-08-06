.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    li   $v0, 5
    syscall
    move $t1, $v0
    li   $v0, 5
    syscall
    move $t2, $v0
    slt  $t3, $t0, $t1
    beq  $t3, $zero, check_third
    move $t0, $t1
check_third:
    slt  $t3, $t0, $t2
    beq  $t3, $zero, max_ready
    move $t0, $t2
max_ready:
    move $a0, $t0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
