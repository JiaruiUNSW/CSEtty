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
    beq $a1,$zero,mf0
    lw $t4,0($a0)
    li $v0,0
    li $t2,1
    addiu $t0,$a0,4
    mf1: beq $t2,$a1,mf9
    lw $t3,0($t0)
    slt $t5,$t4,$t3
    beq $t5,$zero,mf2
    move $t4,$t3
    move $v0,$t2
    mf2: addiu $t2,$t2,1
    addiu $t0,$t0,4
    b mf1
    mf0: li $v0,-1
    mf9: jr $ra
