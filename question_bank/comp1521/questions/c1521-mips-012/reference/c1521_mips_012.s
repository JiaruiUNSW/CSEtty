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
    beq $a1,$zero,mg0
    lw $t4,0($a0)
    move $t5,$t4
    addiu $t0,$a0,4
    addiu $t1,$a1,-1
    mg1: beq $t1,$zero,mg8
    lw $t3,0($t0)
    slt $t6,$t3,$t4
    beq $t6,$zero,mg2
    move $t4,$t3
    mg2: slt $t6,$t5,$t3
    beq $t6,$zero,mg3
    move $t5,$t3
    mg3: addiu $t0,$t0,4
    addiu $t1,$t1,-1
    b mg1
    mg8: subu $v0,$t5,$t4
    jr $ra
    mg0: li $v0,0
    jr $ra
