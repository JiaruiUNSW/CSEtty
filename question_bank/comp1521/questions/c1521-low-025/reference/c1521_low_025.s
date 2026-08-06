.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    move $t1, $zero
    move $t2, $zero
    move $t3, $zero
record_loop:
    slt  $t4, $t1, $t0
    beq  $t4, $zero, records_done
    li   $v0, 5
    syscall
    andi $t5, $v0, 255
    addu $t2, $t2, $t5
    srl  $t6, $v0, 8
    andi $t6, $t6, 255
    sll  $t6, $t6, 24
    sra  $t6, $t6, 24
    addu $t3, $t3, $t6
    addiu $t1, $t1, 1
    b    record_loop
records_done:
    move $a0, $t2
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    move $a0, $t3
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
