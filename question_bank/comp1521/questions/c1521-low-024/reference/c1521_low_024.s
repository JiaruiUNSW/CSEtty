.text
.globl main
main:
    li   $v0, 5
    syscall
    move $a0, $v0
    jal  triangular
    move $a0, $v0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall

triangular:
    bne  $a0, $zero, triangular_recursive
    move $v0, $zero
    jr   $ra
triangular_recursive:
    addiu $sp, $sp, -8
    sw   $ra, 4($sp)
    sw   $a0, 0($sp)
    addiu $a0, $a0, -1
    jal  triangular
    lw   $t0, 0($sp)
    lw   $ra, 4($sp)
    addiu $sp, $sp, 8
    addu $v0, $v0, $t0
    jr   $ra
