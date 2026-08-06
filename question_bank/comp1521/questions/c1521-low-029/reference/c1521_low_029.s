.data
.align 2
sorted_values: .space 64
.text
.globl main
main:
    li   $v0, 5
    syscall
    move $s0, $v0
    li   $v0, 5
    syscall
    move $s1, $v0
    la   $s2, sorted_values
    move $t0, $zero
read_sorted:
    slt  $t1, $t0, $s0
    beq  $t1, $zero, call_search
    li   $v0, 5
    syscall
    sll  $t2, $t0, 2
    addu $t3, $s2, $t2
    sw   $v0, 0($t3)
    addiu $t0, $t0, 1
    b    read_sorted
call_search:
    move $a0, $s2
    move $a1, $zero
    addiu $a2, $s0, -1
    move $a3, $s1
    jal  binary_search
    move $a0, $v0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall

binary_search:
    addiu $sp, $sp, -20
    sw   $ra, 16($sp)
    sw   $a0, 12($sp)
    sw   $a1, 8($sp)
    sw   $a2, 4($sp)
    sw   $a3, 0($sp)
    slt  $t0, $a2, $a1
    bne  $t0, $zero, search_absent
    subu $t1, $a2, $a1
    srl  $t1, $t1, 1
    addu $t1, $t1, $a1
    sll  $t2, $t1, 2
    addu $t2, $a0, $t2
    lw   $t3, 0($t2)
    beq  $t3, $a3, search_found
    slt  $t0, $a3, $t3
    beq  $t0, $zero, search_right
    addiu $a2, $t1, -1
    jal  binary_search
    b    search_return
search_right:
    addiu $a1, $t1, 1
    jal  binary_search
    b    search_return
search_found:
    move $v0, $t1
    b    search_return
search_absent:
    li   $v0, -1
search_return:
    lw   $a3, 0($sp)
    lw   $a2, 4($sp)
    lw   $a1, 8($sp)
    lw   $a0, 12($sp)
    lw   $ra, 16($sp)
    addiu $sp, $sp, 20
    jr   $ra
