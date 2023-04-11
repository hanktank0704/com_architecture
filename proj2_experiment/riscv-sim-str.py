x = [0 for i in range(32)] # registers
N=0 # how many instructions


def divide_list(list):
    for i in range(0, len(list), 32):
        yield list[i:i+32]

def put_zero_front_hex(a):
    if(a<0):
        temp = pow(2,32) + a
        return '0x' + hex(int(temp))[2:].zfill(8)
    return '0x' + hex(int(a))[2:].zfill(8)


import sys
infile = sys.argv[1]

f = open(infile, "rb")
filecontents = f.readlines()

N = int(sys.argv[2])     # get N

bit_list=[] #all bit in one list
initial_instr_list=[]    #32bit each list
instr_num = 0

# print(type(filecontents))
# print(type(filecontents[0]))
# print(type(filecontents[0][0]))

for i in filecontents:
    count = 0
    for j in i:
        k = format(j, '08b')

        for a in k:
            bit_list.append(int(a))

risc_list = list(divide_list(bit_list))

instr_list = []
for i in risc_list:
    for j in range(0, 8):
        i[j], i[j+24] = i[j+24], i[j]
        i[j+8], i[j+16] = i[j+16], i[j+8]
    temp_instr_list = []
    for digit in range(len(i)):
        temp_instr_list.append(str(i[digit]))

    temp_instr = "".join(temp_instr_list)
    instr_list.append(temp_instr)


# print(instr_list)
# sys.exit(1)


#for i in filecontents:
#    count = 0
#    k_list = []
#    for j in i:
#        print(j)
#        k = format(j, '08b')
#        print(k)
#        print(type(k))
#        count += 1
#        if count % 4 == 0:
#            k_list.append(k)
#            initial_instr = "".join(k_list)
#            initial_instr_list.append(initial_instr)
#            k_list = []
#        else:
#            k_list.append(k)
#    
#        for a in k:
#            bit_list.append(int(a))
        

# instr_list = list(divide_list(bit_list))

# for i in instr_list:
#     for j in i:
#         print(j, end="")
#     print()


#instr_list=[]    #32bit each list
#for initial_instr in initial_instr_list:
#    temp_instr_list = []
#    for digit in range(8):
#        temp_instr_list.append(initial_instr[24+digit])
#
#    for digit in range(8):
#        temp_instr_list.append(initial_instr[16+digit])
#
#    for digit in range(8):
#        temp_instr_list.append(initial_instr[8+digit])
#
#    for digit in range(8):
#        temp_instr_list.append(initial_instr[0+digit])
#
#    instr_str = "".join(temp_instr_list)
#    instr_list.append(instr_str)

#        temp = instr[digit]
#        instr[digit] = instr[digit+24]
#        instr[digit+24] = temp
#
#        temp = instr[digit+8]
#        instr[digit+8] = instr[digit+16]
#        instr[digit+16] = temp
#        instr[digit], instr[digit + 24] = instr[digit + 24], instr[digit]
#        instr[digit+8], instr[digit + 16] = instr[digit + 16], instr[digit+8]

# print()
# for i in instr_list:
#     for j in i:
#         print(j, end="")
#     print()

# print(type(instr_list[0][1]))
# print(type(instr_list[0]))

instr_cnt = 0


if(len(instr_list) < N):
    print("No more instructions")

for instr in instr_list:

    if(instr_cnt == N):
        break
    instr_cnt += 1

    temp_hex = 0
    num = 0
    hex_list= []
    final_hex = ""

#    for binary_digit in instr:
#        temp_hex = 2 * temp_hex + int(binary_digit)
#        num += 1
#        if num%4 == 0:
#            hex_list.append(hex(temp_hex)[2:])
#            temp_hex = 0
#
#    final_hex = "".join(map(str,hex_list))

    final_hex = format(int(instr, 2), '4x')
    

#    if instr[25] == 0 and instr[26] == 1 and instr[27] == 1 and instr[28] == 0 and instr[29] == 1 and instr[30] == 1 and instr[31] == 1 : # lui opcode = 0110111
    
    if instr[25:32] == "0110111":

        rd = 0
        imm = 0

#        for a in instr[20:25]:
#            rd = rd * 2 + a

        rd = int(instr[20:25], 2)
        
        if int(instr[0]) == 0:
            imm = int(instr[0:20], 2)
#            for a in instr[0:20]:
#                imm = imm * 2 + a
        else:
            for a in instr[0:20]:
                imm = imm * 2 + (1-int(a))
            imm = -(imm + 1)

       #*******************************왜 하는 지 모르겟음 
        imm = imm * 4096
        #***********************************

        # print(f"inst {instr_num}: {final_hex} lui x{rd}, {imm}")
        instr_num +=1


        x[rd] = imm 
    
#    elif instr[25] == 0 and instr[26] == 0 and instr[27] == 1 and instr[28] == 0 and instr[29] == 1 and instr[30] == 1 and instr[31] == 1 : # auipc 0010111
    elif instr[25:32] == "0010111":

        rd = 0
        imm = 0

        rd = int(instr[20:25], 2)
#        for a in instr[20:25]:
#            rd = rd * 2 + a
        
        if int(instr[0]) == 0:
            imm = int(instr[0:20], 2)
#            for a in instr[0:20]:
#                imm = imm * 2 + a
        else:
            for a in instr[0:20]:
                imm = imm * 2 + (1-int(a))
            imm = -(imm + 1)

        imm = imm * 4096

        # print(f"inst {instr_num}: {final_hex} auipc x{rd}, {imm}")

        instr_num +=1

#    elif instr[25] == 1 and instr[26] == 1 and instr[27] == 0 and instr[28] == 1 and instr[29] == 1 and instr[30] == 1 and instr[31] == 1 : # jal 1101111
    elif instr[25:32] == "1101111":

        rd = 0
        imm = 0

        rd = int(instr[20:25], 2)
#        for a in instr[20:25]:
#            rd = rd * 2 + a
        
        if int(instr[0]) == 0:
            imm1 = int(instr[12:20], 2)
#            for a in instr[12:20]:
#                imm = imm * 2 + a
            imm1 = imm1 * 2 + int(instr[11])

            imm2 = int(instr[1:11], 2)
#            for a in instr[1:11]:
#                imm = imm * 2 + a
            imm = imm1 * 1024 + imm2
        else:
            for a in instr[12:20]:
                imm = imm * 2 + (1 - int(a))
            imm = imm * 2 + (1 - int(instr[11]))
            for a in instr[1:11]:
                imm = imm * 2 + (1 - int(a))
            imm = -(imm + 1)
        
        #******************************왜 *2 하는지 모르겠음
        imm = imm * 2
        #******************************왜 *2 하는지 모르겠음

        # print(f"inst {instr_num}: {final_hex} jal x{rd}, {imm}")

        instr_num +=1

#    elif instr[25] == 1 and instr[26] == 1 and instr[27] == 0 and instr[28] == 0 and instr[29] == 1 and instr[30] == 1 and instr[31] == 1 : # jalr 1100111
    elif instr[25:32] == "1100111":

        rd = 0
        rs1 = 0
        imm = 0

#        for a in instr[20:25]:
#            rd = rd * 2 + a
        rd = int(instr[20:25], 2)
        
#        for a in instr[12:17]:
#            rs1 = rs1 * 2 + a
        rs1 = int(instr[12:17], 2)

        if int(instr[0]) == 0:
            for a in instr[1:12]:
                imm = imm * 2 + int(a)
        else:
            for a in instr[1:12]:
                imm = imm * 2 + (1-int(a))
            imm = -(imm + 1)

        # print(f"inst {instr_num}: {final_hex} jalr x{rd}, {imm}(x{rs1})")

        instr_num +=1

#    elif instr[25] == 1 and instr[26] == 1 and instr[27] == 0 and instr[28] == 0 and instr[29] == 0 and instr[30] == 1 and instr[31] == 1 : # beq ~ bgeu 1100011
    elif instr[25:32] == "1100011":

        rs1 = 0
        rs2 = 0
        imm = 0

#        for a in instr[12:17]:
#            rs1 = rs1 * 2 + a
        rs1 = int(instr[12:17], 2)

#        for a in instr[7:12]:
#            rs2 = rs2 * 2 + a
        rs2 = int(instr[7:12], 2)

        if int(instr[0]) == 0:
            imm = imm * 2 + int(instr[24])
            for a in instr[1:7]:
                imm = imm * 2 + int(a)
            for a in instr[20:25]:
                imm = imm * 2 + int(a)

        else:
            imm = imm * 2 + (1 - int(instr[24]))
            for a in instr[1:7]:
                imm = imm * 2 + (1-int(a))
            for a in instr[20:25]:
                imm = imm * 2 + (1-int(a))
            imm = -(imm + 1)

            #*************************왜 또 -1 하는지 모르겠음
            imm = imm - 1
            #*************************왜 또 -1 하는지 모르겠음

        if instr[17:20] == "000":
            # print(f"inst {instr_num}: {final_hex} beq x{rs1}, x{rs2}, {imm}")
            pass

        if instr[17:20] == "001":
            # print(f"inst {instr_num}: {final_hex} bne x{rs1}, x{rs2}, {imm}")
            pass

        if instr[17:20] == "100":
            # print(f"inst {instr_num}: {final_hex} blt x{rs1}, x{rs2}, {imm}")
            pass

        if instr[17:20] == "101":
            # print(f"inst {instr_num}: {final_hex} bge x{rs1}, x{rs2}, {imm}")
            pass
        if instr[17:20] == "110":
            # print(f"inst {instr_num}: {final_hex} bltu x{rs1}, x{rs2}, {imm}")
            pass

        if instr[17:20] == "111":
            # print(f"inst {instr_num}: {final_hex} bgeu x{rs1}, x{rs2}, {imm}")
            pass

        instr_num +=1

#    elif instr[25] == 0 and instr[26] == 0 and instr[27] == 0 and instr[28] == 0 and instr[29] == 0 and instr[30] == 1 and instr[31] == 1 : # LB ~ lhu 0000011
    elif instr[25:32] == "0000011":

        rd = 0
        rs1 = 0
        imm = 0

        rd = int(instr[20:25], 2)
#        for a in instr[20:25]:
#            rd = rd * 2 + a
        
        rs1 = int(instr[12:17], 2)
#        for a in instr[12:17]:
#            rs1 = rs1 * 2 + a

        if int(instr[0]) == 0:
            for a in instr[1:12]:
                imm = imm * 2 + int(a)
        else:
            for a in instr[1:12]:
                imm = imm * 2 + (1-int(a))
            imm = -(imm + 1)

        if instr[17:20] == "000":
            # print(f"inst {instr_num}: {final_hex} lb x{rd}, {imm}(x{rs1})")
            pass
        
        if instr[17:20] == "001":
            # print(f"inst {instr_num}: {final_hex} lh x{rd}, {imm}(x{rs1})")
            pass

        if instr[17:20] == "010":
            # print(f"inst {instr_num}: {final_hex} lw x{rd}, {imm}(x{rs1})")
            pass

        if instr[17:20] == "100":
            # print(f"inst {instr_num}: {final_hex} lbu x{rd}, {imm}(x{rs1})")
            pass

        if instr[17:20] == "101":
            # print(f"inst {instr_num}: {final_hex} lhu x{rd}, {imm}(x{rs1})")
            pass

        instr_num +=1

#    elif instr[25] == 0 and instr[26] == 1 and instr[27] == 0 and instr[28] == 0 and instr[29] == 0 and instr[30] == 1 and instr[31] == 1 : # sb ~ sw 0100011
    elif instr[25:32] == "0100011":

        rs1 = 0
        rs2 = 0
        imm = 0

        rs1 = int(instr[12:17], 2)
#        for a in instr[12:17]:
#            rs1 = rs1 * 2 + a

        rs2 = int(instr[7:12], 2)
#        for a in instr[7:12]:
#            rs2 = rs2 * 2 + a

        if int(instr[0]) == 0:
            for a in instr[1:7]:
                imm = imm * 2 + int(a)
            for b in instr[20:25]:
                imm = imm * 2 + int(b)

        else:
            for a in instr[1:7]:
                imm = imm * 2 + (1-int(a))
            for b in instr[20:25]:
                imm = imm * 2 + (1-int(b))
            imm = -(imm + 1)

        if instr[17:20] == "000":
            # print(f"inst {instr_num}: {final_hex} sb x{rs2}, {imm}(x{rs1})")
            pass

        if instr[17:20] == "001":
            #print(f"inst {instr_num}: {final_hex} sh x{rs2}, {imm}(x{rs1})")
            pass

        if instr[17:20] == "010":
            #print(f"inst {instr_num}: {final_hex} sw x{rs2}, {imm}(x{rs1})")
            pass

        instr_num +=1

#    elif instr[25] == 0 and instr[26] == 0 and instr[27] == 1 and instr[28] == 0 and instr[29] == 0 and instr[30] == 1 and instr[31] == 1 : # addi ~ srai 0010011
    elif instr[25:32] == "0010011":
        rd = 0
        rs1 = 0
        shamt = 0
        imm = 0
        unsigned_imm = 0

        rd = int(instr[20:25], 2)
#        for a in instr[20:25]:
#            rd = rd * 2 + a
        
        rs1 = int(instr[12:17], 2)
#        for a in instr[12:17]:
#            rs1 = rs1 * 2 + a

        shamt = int(instr[7:12], 2)
#        for a in instr[7:12]:
#            shamt = shamt * 2 + a

        if int(instr[0]) == 0:
            for a in instr[1:12]:
                imm = imm * 2 + int(a)
        else:
            for a in instr[1:12]:
                imm = imm * 2 + (1-int(a))
            imm = -(imm + 1)
        
        unsigned_imm = int(instr[0:12], 2)
#        for a in instr[0:12]:
#            unsigned_imm = unsigned_imm * 2 + a

        if instr[17:20] == "001":
            if instr[0:7] == "0000000":
                #print(f"inst {instr_num}: {final_hex} slli x{rd}, x{rs1}, {shamt}")
                if(x[rs1]<0):
                    x[rd] = (x[rs1] << shamt) % (-pow(2,32))

                else:
                    x[rd] = (x[rs1] << shamt) % pow(2,32)
                # x[rd] = x[rs1]
                # for j in range(shamt):
                #     x[rd] = x[rd] * 2

        if instr[17:20] == "101":
            if instr[0:7] == "0000000":
                #print(f"inst {instr_num}: {final_hex} srli x{rd}, x{rs1}, {shamt}")

######################################################
                if(x[rs1] < 0):
                    temp = put_zero_front_hex(x[rs1])
                    num = 0
                    for aa in temp[2:]:
                        num = num * 16 + int(aa,16)

                    x[rd] = num / pow(2,shamt)
                else:
                    x[rd] = x[rs1]
                    for j in range(shamt):
                        x[rd] = x[rd] / 2

            if instr[0:7] == "0100000":
                #print(f"inst {instr_num}: {final_hex} srai x{rd}, x{rs1}, {shamt}")

                x[rd] = int(x[rs1] / pow(2,shamt))
                
        if instr[17:20] == "000":
            #print(f"inst {instr_num}: {final_hex} addi x{rd}, x{rs1}, {imm}")

            x[rd] = x[rs1] + imm
        
        if instr[17:20] == "010":
            #print(f"inst {instr_num}: {final_hex} slti x{rd}, x{rs1}, {imm}")

            if(x[rs1] < imm):
                x[rd] = 1
            else:
                x[rd] = 0

        if instr[17:20] == "011":
            #print(f"inst {instr_num}: {final_hex} sltiu x{rd}, x{rs1}, {imm}")

#######################################
            temp_rs1 = x[rs1]

            if(x[rs1] < 0):
                temp = put_zero_front_hex(x[rs1])
                num = 0
                for aa in temp[2:]:
                    num = num * 16 + int(aa,16)
                
                temp_rs1 = num

            if(imm<0):
                temp = put_zero_front_hex(imm)
                num=0
                for aa in temp[2:]:
                    num = num * 16 + int(aa,16)
                
                temp_imm = num
            else:
                temp_imm = imm

            #print(f"temp_rs1: {temp_rs1}, unsigned_imm: {unsigned_imm}")
            if(temp_rs1 < temp_imm):
                x[rd] = 1
            else:
                x[rd] = 0
            ############
            # slti 와 차이 찾기

        if instr[17:20] == "100":
            #print(f"inst {instr_num}: {final_hex} xori x{rd}, x{rs1}, {imm}")

            x[rd] = x[rs1] ^ imm

        if instr[17:20] == "110":
            #print(f"inst {instr_num}: {final_hex} ori x{rd}, x{rs1}, {imm}")

            x[rd] = x[rs1] | imm

        if instr[17:20] == "111":
            #print(f"inst {instr_num}: {final_hex} andi x{rd}, x{rs1}, {imm}")

            x[rd] = x[rs1] & imm

        instr_num +=1

#    elif instr[25] == 0 and instr[26] == 1 and instr[27] == 1 and instr[28] == 0 and instr[29] == 0 and instr[30] == 1 and instr[31] == 1 : # add ~ and 0110011
    elif instr[25:32] == "0110011":
        rd = 0
        rs1 = 0
        rs2 = 0

        rd = int(instr[20:25], 2)
        rs1 = int(instr[12:17], 2)
        rs2 = int(instr[7:12], 2)
#        for a in instr[20:25]:
#            rd = rd * 2 + a
#        
#        for a in instr[12:17]:
#            rs1 = rs1 * 2 + a
#        
#        for a in instr[7:12]:
#            rs2 = rs2 * 2 + a


        if instr[17:20] == "000":
            if instr[0:7] == "0000000":
                #print(f"inst {instr_num}: {final_hex} add x{rd}, x{rs1}, x{rs2}")

                x[rd] = x[rs1] + x[rs2]

            if instr[0:7] == "0100000":
                #print(f"inst {instr_num}: {final_hex} sub x{rd}, x{rs1}, x{rs2}")

                x[rd] = x[rs1] - x[rs2]

        if instr[17:20] == "001":
            if instr[0:7] == "0000000":
                #print(f"inst {instr_num}: {final_hex} sll x{rd}, x{rs1}, x{rs2}")

                x[rd] = x[rs1] * pow(2, x[rs2])

        if instr[17:20] == "010":
            if instr[0:7] == "0000000":
                #print(f"inst {instr_num}: {final_hex} slt x{rd}, x{rs1}, x{rs2}")


                if(x[rs1] < x[rs2]):
                    x[rd] = 1
                else:
                    x[rd] = 0

        if instr[17:20] == "011":
            if instr[0:7] == "0000000":
                #print(f"inst {instr_num}: {final_hex} sltu x{rd}, x{rs1}, x{rs2}")
                
                temp_rs1 = x[rs1]
                temp_rs2 = x[rs2]

                if(x[rs1] < 0):
                    temp = put_zero_front_hex(x[rs1])
                    num = 0
                    for aa in temp[2:]:
                        num = num * 16 + int(aa,16)

                    temp_rs1 = num
                if(x[rs2] < 0):
                    temp = put_zero_front_hex(x[rs2])
                    num = 0
                    for aa in temp[2:]:
                        num = num*16 + int(aa,16)

                    temp_rs2 = num

                if(temp_rs1 < temp_rs2):
                    x[rd] = 1
                else:
                    x[rd] = 0

                

        if instr[17:20] == "100":
            if instr[0:7] == "0000000":
                #print(f"inst {instr_num}: {final_hex} xor x{rd}, x{rs1}, x{rs2}")

                x[rd] = int(x[rs1]) ^ int(x[rs2])

        if instr[17:20] == "101":
            if instr[0:7] == "0000000":
                #print(f"inst {instr_num}: {final_hex} srl x{rd}, x{rs1}, x{rs2}")

                if(x[rs1] < 0):
                    temp = put_zero_front_hex(x[rs1])
                    num = 0
                    for aa in temp[2:]:
                        num = num * 16 + int(aa,16)

                    x[rd] = num / (pow(2,x[rs2]))
                else:
                    #print(f"rs1: {x[rs1]} rs2: {x[rs2]}")
                    x[rd] = (x[rs1] / pow(2,x[rs2]))

            if instr[0:7] == "0100000":
                #print(f"inst {instr_num}: {final_hex} sra x{rd}, x{rs1}, x{rs2}")

#                x[rd] = x[rs1]

#                if(x[rs2]<0):
#                    continue
                if(x[rs2] < -32):
                    x[rd] = 0
                    continue
                if(x[rs2] > 32):
                    x[rd] = 0
                    continue

                if(x[rs1]<0):
#                    x[rd] = x[rs1]
                    x[rd] = (x[rs1] / pow(2,x[rs2])) % (-pow(2,32))
                else:
                    #print(x[rs2])
                    x[rd] = (x[rs1] / pow(2, x[rs2])) % pow(2,32)

        if instr[17:20] == "110":
            if instr[0:7] == "0000000":
                #print(f"inst {instr_num}: {final_hex} or x{rd}, x{rs1}, x{rs2}")

                x[rd] = int(x[rs1]) | int(x[rs2])

        if instr[17:20] == "111":
            if instr[0:7] == "0000000":
                #print(f"inst {instr_num}: {final_hex} and x{rd}, x{rs1}, x{rs2}")

                x[rd] = int(x[rs1]) & int(x[rs2])
        instr_num +=1


    else:
        #print(f"inst {instr_num}: {final_hex} unknown instruction")
        instr_num +=1

    x[0] = 0
    for i in range(32):
        x[i] = int(x[i])

x[0] = 0

for i in range(32):
    print(f"x{i}: {put_zero_front_hex(x[i])}")
