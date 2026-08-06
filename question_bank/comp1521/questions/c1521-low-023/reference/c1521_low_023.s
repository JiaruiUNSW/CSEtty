.data
.align 2
array_a: .space 48
array_b: .space 48
.text
.globl main
main:
    li   $v0, 5
    syscall
    move $s0, $v0
    la   $s1, array_a
    la   $s2, array_b
    move $t0, $zero
read_array_a:
    slt  $t1, $t0, $s0
    beq  $t1, $zero, begin_array_b
    li   $v0, 5
    syscall
    sll  $t2, $t0, 2
    addu $t3, $s1, $t2
    sw   $v0, 0($t3)
    addiu $t0, $t0, 1
    b    read_array_a
begin_array_b:
    move $t0, $zero
read_array_b:
    slt  $t1, $t0, $s0
    beq  $t1, $zero, call_distance
    li   $v0, 5
    syscall
    sll  $t2, $t0, 2
    addu $t3, $s2, $t2
    sw   $v0, 0($t3)
    addiu $t0, $t0, 1
    b    read_array_b
call_distance:
    move $a0, $s1
    move $a1, $s2
    move $a2, $s0
    jal  array_distance
    move $a0, $v0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall

array_distance:
    addiu $sp, $sp, -24
    sw   $ra, 20($sp)
    sw   $s0, 16($sp)
    sw   $s1, 12($sp)
    sw   $s2, 8($sp)
    sw   $s3, 4($sp)
    sw   $s4, 0($sp)
    move $s0, $a0
    move $s1, $a1
    move $s2, $a2
    move $s3, $zero
    move $s4, $zero
distance_loop:
    slt  $t0, $s3, $s2
    beq  $t0, $zero, distance_done
    lw   $t1, 0($s0)
    lw   $t2, 0($s1)
    subu $t3, $t1, $t2
    bgez $t3, distance_positive
    subu $t3, $zero, $t3
distance_positive:
    addu $s4, $s4, $t3
    addiu $s0, $s0, 4
    addiu $s1, $s1, 4
    addiu $s3, $s3, 1
    b    distance_loop
distance_done:
    move $v0, $s4
    lw   $s4, 0($sp)
    lw   $s3, 4($sp)
    lw   $s2, 8($sp)
    lw   $s1, 12($sp)
    lw   $s0, 16($sp)
    lw   $ra, 20($sp)
    addiu $sp, $sp, 24
    jr   $ra
