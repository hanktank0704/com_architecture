#!/bin/bash
for var in $(seq 0 10)
do
	com1=$(./riscv-sim ~swe3005/2022f/proj2/proj2_1.bin $(($var+1)))
	com2=$(~swe3005/2022f/proj2/riscv-sim ~swe3005/2022f/proj2/proj2_1.bin $(($var+1)))
	echo $com1 >myoutput1_$var.txt
	echo $com2 >result1_$var.txt
	com3=$(diff myoutput1_$var.txt result1_$var.txt)
	echo $com3
	echo "checked seq$(($var))"
done
		
