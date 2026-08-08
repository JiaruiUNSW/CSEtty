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
    beq $a1,$zero,mm0
    lw $v0,0($a0)
    addiu $t0,$a0,4
    addiu $t1,$a1,-1
    mm1: beq $t1,$zero,mm9
    lw $t2,0($t0)
    slt $t3,$v0,$t2
    beq $t3,$zero,mm2
    move $v0,$t2
    mm2: addiu $t0,$t0,4
    addiu $t1,$t1,-1
    b mm1
    mm0: li $v0,0
    mm9: jr $ra
