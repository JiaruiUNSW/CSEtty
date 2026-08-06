.text
.globl main
main:
    li   $v0, 5
    syscall
    move $s0, $v0
    move $s1, $zero
    move $s2, $zero
squares_loop:
    slt  $t0, $s1, $s0
    beq  $t0, $zero, squares_done
    li   $v0, 5
    syscall
    move $a0, $v0
    jal  square
    addu $s2, $s2, $v0
    addiu $s1, $s1, 1
    b    squares_loop
squares_done:
    move $a0, $s2
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall

square:
    mult $a0, $a0
    mflo $v0
    jr   $ra
