.data
.align 2
matrix: .space 64
.text
.globl main
main:
    li   $v0, 5
    syscall
    move $s0, $v0
    li   $v0, 5
    syscall
    move $s1, $v0
    mult $s0, $s1
    mflo $s2
    la   $s3, matrix
    move $t0, $zero
read_matrix:
    slt  $t1, $t0, $s2
    beq  $t1, $zero, call_border
    li   $v0, 5
    syscall
    sll  $t2, $t0, 2
    addu $t3, $s3, $t2
    sw   $v0, 0($t3)
    addiu $t0, $t0, 1
    b    read_matrix
call_border:
    move $a0, $s3
    move $a1, $s0
    move $a2, $s1
    jal  border_sum
    move $a0, $v0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall

border_sum:
    move $t0, $zero
    move $t1, $zero
    move $t7, $zero
    addiu $t8, $a1, -1
    addiu $t9, $a2, -1
border_row:
    slt  $t2, $t0, $a1
    beq  $t2, $zero, border_done
    move $t1, $zero
border_col:
    slt  $t2, $t1, $a2
    beq  $t2, $zero, border_next_row
    beq  $t0, $zero, border_add
    beq  $t0, $t8, border_add
    beq  $t1, $zero, border_add
    beq  $t1, $t9, border_add
    b    border_next_col
border_add:
    mult $t0, $a2
    mflo $t3
    addu $t3, $t3, $t1
    sll  $t3, $t3, 2
    addu $t4, $a0, $t3
    lw   $t5, 0($t4)
    addu $t7, $t7, $t5
border_next_col:
    addiu $t1, $t1, 1
    b    border_col
border_next_row:
    addiu $t0, $t0, 1
    b    border_row
border_done:
    move $v0, $t7
    jr   $ra
