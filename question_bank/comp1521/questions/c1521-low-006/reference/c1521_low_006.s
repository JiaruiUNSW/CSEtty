.text
.globl main
main:
    move $t0, $zero
    move $t1, $zero
even_loop:
    li   $t2, 5
    beq  $t0, $t2, even_done
    li   $v0, 5
    syscall
    andi $t3, $v0, 1
    bne  $t3, $zero, even_next
    addiu $t1, $t1, 1
even_next:
    addiu $t0, $t0, 1
    b    even_loop
even_done:
    move $a0, $t1
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
