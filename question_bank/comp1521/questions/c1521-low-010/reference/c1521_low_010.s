.data
.align 2
vector_a: .space 64
.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    move $t1, $zero
    la   $t2, vector_a
read_a:
    slt  $t3, $t1, $t0
    beq  $t3, $zero, start_b
    li   $v0, 5
    syscall
    sll  $t4, $t1, 2
    addu $t5, $t2, $t4
    sw   $v0, 0($t5)
    addiu $t1, $t1, 1
    b    read_a
start_b:
    move $t1, $zero
    move $t6, $zero
dot_loop:
    slt  $t3, $t1, $t0
    beq  $t3, $zero, dot_done
    li   $v0, 5
    syscall
    sll  $t4, $t1, 2
    addu $t5, $t2, $t4
    lw   $t7, 0($t5)
    mult $t7, $v0
    mflo $t8
    addu $t6, $t6, $t8
    addiu $t1, $t1, 1
    b    dot_loop
dot_done:
    move $a0, $t6
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
