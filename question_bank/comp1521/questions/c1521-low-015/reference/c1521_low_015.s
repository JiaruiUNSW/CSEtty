.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    move $t1, $zero
    li   $t2, 48
    slt  $t3, $t0, $t2
    bne  $t3, $zero, check_upper
    li   $t2, 58
    slt  $t3, $t0, $t2
    beq  $t3, $zero, check_upper
    li   $t1, 1
    b    class_ready
check_upper:
    li   $t2, 65
    slt  $t3, $t0, $t2
    bne  $t3, $zero, check_lower
    li   $t2, 91
    slt  $t3, $t0, $t2
    beq  $t3, $zero, check_lower
    li   $t1, 2
    b    class_ready
check_lower:
    li   $t2, 97
    slt  $t3, $t0, $t2
    bne  $t3, $zero, class_ready
    li   $t2, 123
    slt  $t3, $t0, $t2
    beq  $t3, $zero, class_ready
    li   $t1, 3
class_ready:
    move $a0, $t1
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
