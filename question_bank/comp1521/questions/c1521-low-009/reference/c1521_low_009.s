.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    li   $v0, 5
    syscall
    move $t1, $v0
gcd_loop:
    beq  $t1, $zero, gcd_done
    div  $t0, $t1
    mfhi $t2
    move $t0, $t1
    move $t1, $t2
    b    gcd_loop
gcd_done:
    move $a0, $t0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall
