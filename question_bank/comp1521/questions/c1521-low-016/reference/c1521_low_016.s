.data
.align 2
values: .space 64
.text
.globl main
main:
    li   $v0, 5
    syscall
    move $s0, $v0
    la   $s1, values
    move $t0, $zero
read_values:
    slt  $t1, $t0, $s0
    beq  $t1, $zero, call_argmax
    li   $v0, 5
    syscall
    sll  $t2, $t0, 2
    addu $t3, $s1, $t2
    sw   $v0, 0($t3)
    addiu $t0, $t0, 1
    b    read_values
call_argmax:
    move $a0, $s1
    move $a1, $s0
    jal  first_max_index
    move $a0, $v0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall

first_max_index:
    lw   $t0, 0($a0)
    move $t1, $zero
    li   $t2, 1
argmax_loop:
    slt  $t3, $t2, $a1
    beq  $t3, $zero, argmax_done
    sll  $t4, $t2, 2
    addu $t5, $a0, $t4
    lw   $t6, 0($t5)
    slt  $t3, $t0, $t6
    beq  $t3, $zero, argmax_next
    move $t0, $t6
    move $t1, $t2
argmax_next:
    addiu $t2, $t2, 1
    b    argmax_loop
argmax_done:
    move $v0, $t1
    jr   $ra
