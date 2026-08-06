.text
.globl main
main:
    li   $v0, 5
    syscall
    move $a0, $v0
    li   $v0, 5
    syscall
    move $a1, $v0
    li   $v0, 5
    syscall
    move $a2, $v0
    jal  range_width
    move $a0, $v0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall

range_width:
    move $t0, $a0
    move $t1, $a0
    slt  $t2, $a1, $t0
    beq  $t2, $zero, max_second
    move $t0, $a1
max_second:
    slt  $t2, $t1, $a1
    beq  $t2, $zero, min_third
    move $t1, $a1
min_third:
    slt  $t2, $a2, $t0
    beq  $t2, $zero, max_third
    move $t0, $a2
max_third:
    slt  $t2, $t1, $a2
    beq  $t2, $zero, width_ready
    move $t1, $a2
width_ready:
    subu $v0, $t1, $t0
    jr   $ra
