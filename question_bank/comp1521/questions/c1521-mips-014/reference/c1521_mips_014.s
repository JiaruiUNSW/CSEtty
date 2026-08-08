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
    slti $t7,$a1,2
    bne $t7,$zero,mq0
    lw $t2,0($a0)
    addiu $t0,$a0,4
    addiu $t1,$a1,-1
    li $v0,0
    mq1: beq $t1,$zero,mq9
    lw $t3,0($t0)
    bne $t2,$t3,mq2
    addiu $v0,$v0,1
    mq2: move $t2,$t3
    addiu $t0,$t0,4
    addiu $t1,$t1,-1
    b mq1
    mq0: li $v0,0
    mq9: jr $ra
