.data
values: .space 400
.text
.globl main
main:
    li $v0,5
    syscall
    move $s0,$v0
    la $s1,values
    li $t0,0
read_loop:
    beq $t0,$s0,read_done
    li $v0,5
    syscall
    sll $t1,$t0,2
    addu $t2,$s1,$t1
    sw $v0,0($t2)
    addiu $t0,$t0,1
    b read_loop
read_done:
    move $a0,$s1
    move $a1,$s0
    jal solve
    move $a0,$v0
    li $v0,1
    syscall
    li $a0,10
    li $v0,11
    syscall
    li $v0,10
    syscall
solve:
    move $t0,$a0
    move $t1,$a1
    li $v0,0
    mb1: beq $t1,$zero,mb9
    lw $t2,0($t0)
    bgez $t2,mb2
    subu $t2,$zero,$t2
    mb2: addu $v0,$v0,$t2
    addiu $t0,$t0,4
    addiu $t1,$t1,-1
    b mb1
    mb9: jr $ra
