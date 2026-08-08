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
    beq $a1,$zero,mi0
    lw $v0,0($a0)
    addiu $t0,$a0,4
    addiu $t1,$a1,-1
    mi1: beq $t1,$zero,mi9
    lw $t2,0($t0)
    slt $t3,$t2,$v0
    beq $t3,$zero,mi2
    move $v0,$t2
    mi2: addiu $t0,$t0,4
    addiu $t1,$t1,-1
    b mi1
    mi0: li $v0,0
    mi9: jr $ra
