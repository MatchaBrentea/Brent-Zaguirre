.text
.macro newline()
	la $a0, 10
	li $v0, 11
	syscall	
.end_macro

.macro space()
	la $a0, 32
	li $v0, 11
	syscall
.end_macro

.macro do_file(%label,%str,%val)
alpha:
	li $t0, 0
	li $t1, 10
	li $t2, 0
	b alpha_loop

alpha_loop:
	lb $t3, %label($t0)
	beq $t3, $t1, rep_null
	add $t0, $t0, 1
	b alpha_loop

rep_null:
	sb $t2, %label($t0)
	b open_file

open_file:
	ctrl_o(%label,0)
	b read_file
	
read_file:
	ctrl_r(%str,%val)
.end_macro

.macro word_trans(%reg1,%reg2)
	jal ex_gate_2
	li $t1, 0
	add %reg1,%reg1,1
	add %reg2,%reg2,1
.end_macro

.macro inp_str(%label,%max)
	la $a0, %label
	li $a1, %max
	li $v0 8
	syscall
.end_macro

.macro ctrl_o(%label,%val)
	li $v0, 13
	la $a0, %label
	li $a1, %val
	li $a2, 0
	syscall
	move $t0, $v0
.end_macro

.macro ctrl_r(%str,%val)
	li $v0, 14
	move $a0, $t0
	la $a1, %str
	li $a2, %val
	syscall
.end_macro

.macro ctrl_w()
	li $v0, 16
	move $a0, $t0
	syscall
.end_macro

.macro print_str(%label)
	la $a0, %label
	li $v0, 4
	syscall
.end_macro

.macro print_char(%reg)
	add $a0, %reg, $zero
	li $v0, 11
	syscall
.end_macro

.macro print_int(%reg)
	add $a0, %reg, $zero
	li $v0, 1
	syscall
.end_macro

.macro input_mode()
	li $v0, 5
	syscall
.end_macro

.macro for_money()
	div $k1, $k0
	mflo $s5
	mfhi $s4
	move $a0, $s5
	li $v0, 1
	syscall
	move $a0, $s4
	li $v0, 1
	syscall
.end_macro

.macro trans_money(%val1,%val2,%labnum,%reg)
	li $t1, %val1
	li $v1, 16
	div %reg, $t1 
 	mflo $s0
	mfhi $s1
	mul $k0, $s0, $v1
	li $t1, %val2
	div $s1, $t1
	mflo $k1
	mfhi $t3
	add $a1, $k0, $k1
	sb $a1, buff+%labnum
.end_macro

.macro for_badge(%reg,%val)
	and %reg, $t0, %val
.end_macro

.macro trans_badge(%val)
	li $k1, %val
	lb $a1, badge($k0)
	add $k0,$k0,1
	jal gate_8
.end_macro

.macro for_ndig(%val)
	li $v1, %val
	lbu $t4, bag($v1)		#t4 = (quan full) hundreth digit
	add $v1, $v1, 1
	lbu $t5, bag($v1)		#t5 = (quan full) tenth digit
	beq $t5, 10, only_one
	add $v1, $v1, 1
	lbu $t6, bag($v1)		#t6 = (quan full) unit digit
	beq $t6, 10, only_two
	sub $t4, $t4, 48
	mul $t4, $t4, 100
	sub $t5, $t5, 48
	mul $t5, $t5, 10
	sub $t6, $t6, 48
	add $s2, $t4, $t5
	add $s2, $s2, $t6		#s2 = (complete) item num
	jr $ra
.end_macro

.macro hex_holder(%reg,%val)
	div $s1, %reg
	mfhi $s1
	mflo $s2
	sb $s2, hex_hold+%val
.end_macro
#=========================================================#

#*********************************#
#	           INITIAL 			  #
#=================================#
true_gate:
	inp_str(file_rom,49)
	inp_str(file_save,49)
	do_file(file_rom,buff2,1048600)	
	ctrl_w()
	do_file(file_save,buff,35000)
	ctrl_w()
	li $t1, 0
	li $t2, 0
	b main


#*********************************#
#	           MAIN	  			  #
#=================================#

main:
	#NAME	= init_1
	#MONEY	= init_2
	#BADGE	= init_3
	#ITEM	= init_4
	#TITLE	= init_5
	#SEARCH = init_6
	#MOM	= init_7
	input_mode()
	beq $v0, 1, init_1
	beq $v0, 2, init_2
	beq $v0, 3, init_3
	beq $v0, 4, init_4
	beq $v0, 5, init_5
	beq $v0, 6, init_6
	beq $v0, 7, init_7
################|RAM|##################

#*********************************#
#	          NAME				  #
#=================================#
init_1:
	li $k0, 0x2598
	b gate_0

gate_0:
	beq $k0, 9631, gate_1
	lbu $k1, buff($k0)
	lb $s7, pokecode($k1)
	beq $s7, 38, gate_1
	print_char($s7)
	add $k0, $k0, 1
	b gate_0	
	 	 	 
gate_1:
	newline()
	li $v0, 8
	la $a0, name
	li $a1,9
	syscall
	li $t0, 0
	li $t1, 0
	li $t2, 9624
	b gate_2
	
gate_2:
	word_trans($t0,$t2)
	word_trans($t0,$t2)
	word_trans($t0,$t2)
	word_trans($t0,$t2)
	word_trans($t0,$t2)
	word_trans($t0,$t2)
	word_trans($t0,$t2)
	b checkpoint_v1
	
ex_gate_2:
	lb $t3, name($t0)
	lb $t4, pokecode($t1)
	beq $t3, 0xa, condition1
	beq $t3,$t4,recaller
	add $t1, $t1, 1
	b ex_gate_2
	
condition1: 
	li $t5, 0x50
	lb $t6, buff($t2)
	sb $t5, buff($t2)
	add $t2, $t2, 1
	b condition2

condition2:
	li $t5, 0
	beq $t2, 9632, checkpoint_v1
	lb $t6, buff($t2)
	sb $t5, buff($t2)
	add $t2, $t2, 1
	b condition2
	
recaller:
	lb $t6, buff($t2)
	sb $t1, buff($t2)
	jr $ra

#*********************************#
#	      	   MONEY			  #
#=================================#
init_2:
	li $s7, 10000
	li $s6, 100
	b gate_3
	
gate_3:
	li $k0, 16
	lbu $k1, buff+9715
	jal money_chk_1
	lbu $k1, buff+9716
	for_money()
	lbu $k1, buff+9717
	for_money()
	newline()
	b gate_4
	
money_chk_1:
	print_str(just_p)
	bnez $k1, money_chk_fin
	lbu $k1, buff+9716
	bnez $k1, money_chk_2
	lbu $k1, buff+9717
	bnez $k1, money_chk_3
	li $a0, 0
	li $v0, 1
	syscall
	newline()
	b gate_4
	
money_chk_2:
	for_money()
	lbu $k1, buff+9717
	for_money()
	b gate_4
	
money_chk_3:
	for_money()
	b gate_4
	
money_chk_fin:
	for_money()
	jr $ra
	
gate_4:
	input_mode()
	move $t0, $v0
	trans_money(100000,10000,9715,$t0)
	trans_money(1000,100,9716,$t3)
	trans_money(10,1,9717,$t3)
	b checkpoint_v1
	
#*********************************#
#	      	   BADGE			  #
#=================================#	
init_3:
	lb $t0, buff+9730
	b gate_5

gate_5:
	for_badge($s1,1)
	for_badge($s2,2) 
	for_badge($s3,4)
	for_badge($s4,8)
	for_badge($s5,16)
	for_badge($s6,32)
	for_badge($s7,64)
	for_badge($t9,128)
	b badge_chk
	
badge_chk:
	beqz $t0, b_empty
	bnez $s1, b_earth
	bnez $s2, b_volcano
	bnez $s3, b_marsh
	bnez $s4, b_soul
	bnez $s5, b_rainbow
	bnez $s6, b_thunder
	bnez $s7, b_cascade
	bnez $t9, b_boulder
	li $t0, 0
	newline()
	b gate_6
	
b_boulder:	print_str(boulder)
		li $t9, 0
		b badge_chk 
b_cascade:	print_str(cascade)
		li $s7, 0
		b badge_chk 	
b_thunder:	print_str(thunder)
		li $s6, 0
		b badge_chk 
b_rainbow:	print_str(rainbow)
		li $s5, 0
		b badge_chk 
b_soul:		print_str(soul)
		li $s4, 0
		b badge_chk 
b_marsh:	print_str(marsh)
		li $s3, 0
		b badge_chk 
b_volcano:	print_str(volcano)
		li $s2, 0
		b badge_chk 
b_earth:	print_str(earth)	
		li $s1, 0
		b badge_chk 
b_empty:	print_str(empty)
		newline()
		b gate_6
	
gate_6:
	la $a0, badge
	li $a1, 9
	li $v0, 8
	syscall
	li $k0, 0
	b gate_7

gate_7:
	trans_badge(128)
	trans_badge(64)
	trans_badge(32)
	trans_badge(16)
	trans_badge(8)
	trans_badge(4)
	trans_badge(2)
	trans_badge(1)
	b gate_10

gate_8:
	beq $a1, 49, gate_9
	jr $ra

gate_9:
	add $t0, $t0, $k1
	jr $ra

gate_10:
	sb $t0, buff+9730
	b checkpoint_v1

#*********************************#
#	      	   ITEM 			  #
#=================================#
init_4:
	li $k0, 0x25c9
	li $a2, 0x50
	li $a3, 0xff
	li $v1, 0
	b gate_11

gate_11:
	lbu $s0, buff($k0)		#s0 = distinct items
	beq $s0, $zero, print_none
	add $t0, $k0, 1
	b gate_12

gate_12:
	li $k1, 0x472b
	li $t1, 1
	lbu $s1, buff($t0)		#s1 = item name
	beq $s1, $a3, gate_13
	add $t0, $t0, 1
	lbu $s2, buff($t0)		#s2 = item quantity
	add $t0, $t0, 1
	add $v1, $v1, 1			#v1 = distinct number
	jal dist_num
	jal item_name
	jal print_name
	print_str(x_sym)
	print_int($s2)
	newline()
	b gate_12

print_none:
	print_str(empty)
	b gate_13

dist_num:
	print_int($v1)
	space()
	jr $ra

item_name:
	beq $t1, $s1, reconnect
	lbu $t2, buff2($k1)
	add $k1, $k1, 1
	beq $t2, $a2, do_address
	b item_name

print_name:
	lbu $t2, buff2($k1)
	beq $t2, $a2, reconnect
	add $k1,$k1,1
	lbu $a0, pokecode($t2)
	li $v0,11
	syscall
	b print_name

do_address:
	add $t1, $t1, 1
	b item_name

reconnect:
	jr $ra

gate_13:
	inp_str(bag,13)
	li $v1, 1
	li $a2, 32
	lbu $t0, bag($v1)
	jal dig_count
	b find_unique

find_unique:
	li $k0, 0x25c9
	li $k1, 0xff
	lbu $t0, buff($k0)
	jal if_greater
	mul $t1, $s0, 2
	add $t1, $t1, $k0 		#t1 = item quantity destination
	sub $t2, $t1, 1			#t2 = item number destination
	sb $s1, buff($t2)
	sb $s2, buff($t1)
	lbu $s7, buff($k0)
	mul $s7, $s7, 2
	add $s7, $s7, 1
	add $s7, $s7, $k0
	sb $a3, buff($s7)
	li $a3, 0
	b checkpoint_v1
	

if_greater:
	bgt $s0, $t0, is_greater
	jr $ra

is_greater:
	add $t0, $t0, 1
	sb $t0, buff($k0)
	jr $ra

dig_count:
	beq $t0, $a2, one_dig
	li $v1, 0
	lbu $t0, bag($v1)		#t0 = tenth digit
	add $v1, $v1, 1
	lbu $t1, bag($v1)		#t1 = unit digit
	sub $t0, $t0, 48
	mul $t0, $t0, 10
	sub $t1, $t1, 48
	add $s0, $t0, $t1		#s0 = (complete) unique number
	li $v1, 5
	lbu $t2, bag($v1)		#t2 = (hexa) tenth digit
	add $v1, $v1, 1
	lbu $t3, bag($v1)		#t3 = (hexa) unit digit
	sub $t2, $t2, 48
	mul $t2, $t2, 16
	sub $t3, $t3, 48
	add $s1, $t2, $t3		#s1 = (complete) item type
	for_ndig(8)

one_dig:
	li $v1, 0
	li $t0, 0				#t0 = tenth digit (always 0)
	lbu $t1, bag($v1)		#t1 = unit digit (only value)
	sub $t1, $t1, 48
	add $s0, $t0, $t1		#s0 = (complete) unique number
	li $v1, 4
	lbu $t2, bag($v1)		#t2 = (hexa) tenth digit
	add $v1, $v1, 1
	lbu $t3, bag($v1)		#t3 = (hexa) unit digit
	sub $t2, $t2, 48
	mul $t2, $t2, 16
	sub $t3, $t3, 48
	add $s1, $t2, $t3		#s1 = (complete) item type
	for_ndig(7)


only_one:
	sub $t4, $t4, 48
	add $s2, $t4, $zero 
	jr $ra

only_two:
	sub $t4, $t4, 48
	mul $t4, $t4, 10
	sub $t5, $t5, 48
	add $s2, $t4, $t5
	jr $ra

#*********************************#
#	    	checksum_v1		 	  #
#=================================#
checkpoint_v1:
	li $t0, 0x2598 
	li $t1, 0
	li $a3, 0
	b checkpart_v1

checkpart_v1:
	lbu $t2, buff($t0)
	beq $t0, 0x3523, checksum_v1
	add $a3, $a3, $t2
	add $t0, $t0, 1
	b checkpart_v1
	
checksum_v1:
	li $t3, 256
	not $a3, $a3
	div $a3, $t3
	mfhi $t4
	sb $t4, buff($t0)
	b end_edit_v1
		
end_edit_v1:
	ctrl_o(file_save,1)
	li $v0, 15
	move $a0, $t0
	la $a1, buff
	li $a2, 32768
	syscall
	ctrl_w()
	b exit

################|ROM|##################

#*********************************#
#	       Title Screen		 	  #
#=================================#
init_5:
	li $a2, 0x4399
	li $a3, 0x4588
	li $k0, 0x4598
	li $s0, 0x50
	li $s2, 10
	li $s3, 0
	li $k1, 0x1c214
	lbu $t3, buff2($a2)
	mul $t3, $t3, 10
	add $k1, $k1, $t3
	b temp_2

temp_2:
	lbu $t4, buff2($k1)
	beq $s3, $s2, re_entry
	beq $t4, $s0, re_entry
	add $s3, $s3, 1
	add $k1, $k1, 1
	lbu $t5, pokecode($t4)
	print_char($t5)
	b temp_2

re_entry:
	newline()
	b gate_14

gate_14:
	li $s1, 0
	li $k1, 0x1c214
	beq $a3, $k0, start_done
	lbu $t0, buff2($a3)
	add $a3, $a3, 1
	mul $t0, $t0, 10
	add $k1, $k1, $t0
	jal start_find
	newline()
	b gate_14

start_find:
	lbu $t1, buff2($k1)
	beq $s1, $s2, recall
	beq $t1, $s0, recall
	add $s1, $s1, 1
	add $k1, $k1, 1
	b code_trans

code_trans:
	lbu $t2, pokecode($t1)
	print_char($t2)
	b start_find

recall:
	jr $ra

start_done:
	b exit

#*********************************#
#	    	 Dialogue		 	  #
#=================================#
init_6:
	
	inp_str(dialogue,31)
	li $a2, 0
	li $a3, 0
	li $v1, 0
	li $t9, 0
	b pre_gate_15

pre_gate_15:
	lbu $t8, dialogue($t9)
	beq $t8, $v1, re_gate_15
	add $t9,$t9,1
	b pre_gate_15

re_gate_15:
	sub $t9,$t9,1
	b gate_15
	
gate_15:
	beq $a2, $t9, found_dialogue
	lbu $t0, dialogue($a2)
	lbu $t1, buff2($a3)
	lbu $t2, pokecode($t1)
	beq $t0, $t2, find_dialogue
	li $a2, 0
	li $s0, 0
	add $a3, $a3, 1
	add $v1, $v1, 1
	beq $v1, 1048576, found_dialogue
	b gate_15

find_dialogue:
	add $s0, $a3, $zero
	add $a2, $a2, 1
	add $a3, $a3, 1
	add $v1, $v1, 1
	beq $v1, 1048576, found_dialogue
	b gate_15

found_dialogue:	
	beqz, $s0, not_found
	sub $s0, $s0, $t9
	add $s0, $s0, 1
	li $t8, 268435456
	li $t7, 16777216
	li $t6, 1048576
	li $t5, 65536
	li $t4, 4096
	li $t3, 256
	li $t2, 16
	li $t1, 1 
	li $k0, 0
	print_str(hex_start)
	b gate_16

gate_16:
	div $s0, $t8
	mfhi $s1
	mflo $s2
	sb $s2, hex_hold+0	
	hex_holder($t7,1)
	hex_holder($t6,2)
	hex_holder($t5,3)
	hex_holder($t4,4)
	hex_holder($t3,5)
	hex_holder($t2,6)
	hex_holder($t1,7)
	b gate_17

gate_17:
	lbu $t0, hex_hold($k0)
	bnez $t0, gate_18
	add $k0, $k0, 1
	b gate_17

gate_18:
	beq $k0, 8, exit
	lbu $t0, hex_hold($k0)
	add $k0, $k0, 1
	jal conditions
	b gate_18

conditions:
	beq $t0, 10, store_a
	beq $t0, 11, store_b
	beq $t0, 12, store_c
	beq $t0, 13, store_d
	beq $t0, 14, store_e
	beq $t0, 15, store_f
	print_int($t0)
	jr $ra

store_a:
	li $t0, 97
	print_char($t0)
	jr $ra

store_b:
	li $t0, 98
	print_char($t0)
	jr $ra

store_c:
	li $t0, 99
	print_char($t0)
	jr $ra

store_d:
	li $t0, 100
	print_char($t0)
	jr $ra

store_e:
	li $t0, 101
	print_char($t0)
	jr $ra

store_f:
	li $t0, 102
	print_char($t0)
	jr $ra

not_found:
	print_str(none_found)
	b exit


#*********************************#
#	    	Mom Dialogue	 	  #
#=================================#
init_7:
	li $t1, 0x94b08
	li $t9, 0
	li $s5, 0x94b08
	li $s3, 0x94b08

gate_19:
	lbu $t0, buff2($t1)
	lbu $a0, pokecode($t0)
	print_char($a0)
	beq $a0, 35, gate_20
	add $t1,$t1, 1
	b gate_19

gate_20:
	newline()
	li $v1, 0x94b08
	inp_str(mom_space,151)
	li $s0, 0
	b find_length

find_length:
	lbu $t0, mom_space($s0)
	beq $t0, 10, new_mom
	add $s0, $s0, 1					#s0 = length
	b find_length

new_mom:
	li $t8, 0
	lbu $t2, mom_space($t9)
	jal convert_code
	jal store_mom
	beq $t9, $s0, do_hash
	add $t9, $t9, 1
	b new_mom

do_hash:
	add $s3, $s3, $s0
	li $s1, 0x57
	b fill_hash

fill_hash:
	sb $s1, buff2($s3)
	beq $s3, 0x94b9e, checkpoint_v2
	add $s3, $s3, 1
	b fill_hash

convert_code:
	lbu $t3, pokecode($t8)
	beq $t2, $t3, recall
	add $t8, $t8, 1
	b convert_code

store_mom:
	sb $t8, buff2($s5)
	add $s5, $s5, 1
	b recall


#*********************************#
#	    	checksum_v2		 	  #
#=================================#
checkpoint_v2:
	li $t0, 0x00
	li $t1,0
	li $a3, 0
	li $t8, 0
	li $t9, 0
	b checkpart_v2

checkpart_v2:
	jal if_sum
	lbu $t2, buff2($t0)
	beq $t0, 0x100000, checksum_v2
	add $a3, $a3, $t2
	add $t0,$t0, 1
	b checkpart_v2

if_sum:
	beq $t0, 0x14e, is_sum
	jr $ra

is_sum:
	add $t0, $t0, 2
	jr $ra

checksum_v2:
	li $t0, 0x14e
	sh $a3, buff2($t0)
	lbu $t8, buff2($t0)
	add $t0, $t0, 1
	lbu $t9, buff2($t0)
	sb $t8, buff2($t0)
	li $t0, 0x14e
	sb $t9, buff2($t0)
	b end_edit_v2

end_edit_v2:
	ctrl_o(file_rom,1)
	li $v0, 15
	move $a0, $t0
	la $a1, buff2
	li $a2, 1048576
	syscall
	ctrl_w()
	b exit


#=======================================#
exit:
	li $v0, 10
	syscall	
	
.data
file_save:	.space 50
file_rom:	.space 50
pokecode:	   #0123456789ABCDEF#
		.ascii "^***************" #0
		.ascii "****************" #1
		.ascii "****************" #2
		.ascii "****************" #3
		.ascii "***************"  #4
		.byte 92				  #4f
		.ascii "&|***_*#$*******" #5
		.ascii "****************" #6
		.ascii "*************** " #7
		.ascii "ABCDEFGHIJKLMNOP" #8
		.ascii "QRSTUVWXYZ():;[]" #9
		.ascii "abcdefghijklmnop" #A
		.ascii "qrstuvwxyz@*****" #B
		.ascii "****************" #C
		.ascii "****************" #D
	 	.ascii "'**-**?!.*******" #E
		.ascii "******0123456789" #F
buff:		.space 35000
buff2:		.space 1048600
name:		.space 8
badge:		.space 8
bag:		.space 13
dialogue:	.space 31
hex_hold:	.space 9
mom_space:  .space 152
just_p:		.asciiz "P "
str_name_old:	.asciiz "Stored name: "
str_money_old:	.asciiz "Stored money: "
str_badge_old:	.asciiz "Stored badge: "
thunder:	.asciiz "THUNDERBADGE "
rainbow:	.asciiz "RAINBOWBADGE "
mode:		.asciiz "1.) Name\n2.) Money\n3.) Badge\n4.) Item\n5.) Title Screen Pokemon\n6.) Dialogue search\n7.) Mom's dialogue\n"
input:		.asciiz "Input mode: "
boulder:	.asciiz "BOULDERBADGE "
cascade:	.asciiz "CASCADEBADGE "
soul:		.asciiz "SOULBADGE "
marsh:		.asciiz "MARSHBADGE "
volcano:	.asciiz "VOLCANOBADGE "
earth:		.asciiz "EARTHBADGE "
empty:		.asciiz "EMPTY " 
x_sym:		.asciiz " x"
hex_start:  .asciiz "0x"
none_found:	.asciiz "NOT FOUND"
debug:		.asciiz "DEBUG\n"
