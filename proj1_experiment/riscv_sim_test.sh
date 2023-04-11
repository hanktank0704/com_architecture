#!/bin/sh
echo "message 1"
./riscv-sim /home/swe3005/2022f/proj1/proj1_1.bin > my_output1.txt
echo "message 2"
./riscv-sim /home/swe3005/2022f/proj1/proj1_2.bin > my_output2.txt
echo "message 3"
./riscv-sim /home/swe3005/2022f/proj1/proj1_3.bin > my_output3.txt
echo "message 4"
./riscv-sim /home/swe3005/2022f/proj1/proj1_4.bin > my_output4.txt
echo "message 5"
./riscv-sim /home/swe3005/2022f/proj1/proj1_5.bin > my_output5.txt
echo "message 6"
./riscv-sim /home/swe3005/2022f/proj1/proj1_6.bin > my_output6.txt
echo "message 7"
./riscv-sim /home/swe3005/2022f/proj1/proj1_7.bin > my_output7.txt
echo "my riscv-sim complete!"
/home/swe3005/2022f/proj1/riscv-sim /home/swe3005/2022f/proj1/proj1_1.bin > ref_output1.txt
/home/swe3005/2022f/proj1/riscv-sim /home/swe3005/2022f/proj1/proj1_2.bin > ref_output2.txt
/home/swe3005/2022f/proj1/riscv-sim /home/swe3005/2022f/proj1/proj1_3.bin > ref_output3.txt
/home/swe3005/2022f/proj1/riscv-sim /home/swe3005/2022f/proj1/proj1_4.bin > ref_output4.txt
/home/swe3005/2022f/proj1/riscv-sim /home/swe3005/2022f/proj1/proj1_5.bin > ref_output5.txt
/home/swe3005/2022f/proj1/riscv-sim /home/swe3005/2022f/proj1/proj1_6.bin > ref_output6.txt
/home/swe3005/2022f/proj1/riscv-sim /home/swe3005/2022f/proj1/proj1_7.bin > ref_output7.txt
diff my_output1.txt ref_output1.txt
diff my_output2.txt ref_output2.txt
diff my_output3.txt ref_output3.txt
diff my_output4.txt ref_output4.txt
diff my_output5.txt ref_output5.txt
diff my_output6.txt ref_output6.txt
diff my_output7.txt ref_output7.txt
