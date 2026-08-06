.text
.globl main
main:
    li   $v0, 5
    syscall
    move $t0, $v0
    li   $t1, 4
max_loop:
    li   $v0, 5
    syscall
    ble  $v0, $t0, max_keep
    move $t0, $v0
max_keep:
    addi $t1, $t1, -1
    bnez $t1, max_loop
    move $a0, $t0
    li   $v0, 1
    syscall
    li   $a0, 10
    li   $v0, 11
    syscall
    li   $v0, 10
    syscall

