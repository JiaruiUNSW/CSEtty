.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    move $t1, $zero
    move $t2, $zero
stream_loop:
    slt  $t3, $t1, $t0
    beq  $t3, $zero, stream_done
    li   $v0, 5
    syscall
    addu $t2, $t2, $v0
    addiu $t1, $t1, 1
    b    stream_loop
stream_done:
    move $a0, $t2
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
