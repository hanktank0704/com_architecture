#!/bin/sh
python3 riscv-sim_221106.py /home/swe3005/2022f/proj2/proj2_1.bin 100 > myoutput1.txt
python3 riscv-sim_221106.py /home/swe3005/2022f/proj2/proj2_2.bin 100 > myoutput2.txt
python3 riscv-sim_221106.py /home/swe3005/2022f/proj2/proj2_3.bin 100 > myoutput3.txt
python3 riscv-sim_221106.py /home/swe3005/2022f/proj2/proj2_4.bin 100 > myoutput4.txt
python3 riscv-sim_221106.py /home/swe3005/2022f/proj2/proj2_5.bin 100 > myoutput5.txt

/home/swe3005/2022f/proj2/riscv-sim /home/swe3005/2022f/proj2/proj2_1.bin 100 > answer1.txt
/home/swe3005/2022f/proj2/riscv-sim /home/swe3005/2022f/proj2/proj2_2.bin 100 > answer2.txt
/home/swe3005/2022f/proj2/riscv-sim /home/swe3005/2022f/proj2/proj2_3.bin 100 > answer3.txt
/home/swe3005/2022f/proj2/riscv-sim /home/swe3005/2022f/proj2/proj2_4.bin 100 > answer4.txt
/home/swe3005/2022f/proj2/riscv-sim /home/swe3005/2022f/proj2/proj2_5.bin 100 > answer5.txt

diff answer1.txt myoutput1.txt
diff answer2.txt myoutput2.txt
diff answer3.txt myoutput3.txt
diff answer4.txt myoutput4.txt
diff answer5.txt myoutput5.txt

echo "test finished"
