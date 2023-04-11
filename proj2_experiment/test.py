x = ['0x00000000' for i in range(32)] # registers
N=0 # how many instructions

def s16(value):
    return -(value & 0x80000000) | (value & 0x7fffffff)

# print(s16(int(a,16)))

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
print(N)

bit_list=[] #all bit in one list
risc_list=[]    #32bit each list
risc_int=[]     #int version of risc_list
inst_num = 0

# print(type(filecontents))
# print(type(filecontents[0]))
# print(type(filecontents[0][0]))

for i in filecontents:
    count = 0
    for j in i:
        k = format(j, '08b')
        # print(k)
        # print(type(k))
    
        for a in k:
            bit_list.append(int(a))

risc_list = list(divide_list(bit_list))

# for i in risc_list:
#     for j in i:
#         print(j, end="")
#     print()


for i in risc_list:
    for j in range(0,8):
        i[j], i[j + 24] = i[j + 24], i[j]
        i[j+8], i[j + 16] = i[j + 16], i[j+8]

# print()
# for i in risc_list:
#     for j in i:
#         print(j, end="")
#     print()

# print(type(risc_list[0][1]))
# print(type(risc_list[0]))

what_line_index = 0

if(len(risc_list) < N):
    print("NO more instructions")

for i in risc_list:
    temp_hex = 0
    hex_list= []
    final_hex = ""
    num = 0


    if(what_line_index == N):
        break
    what_line_index+=1

    for a in i:
        temp_hex = 2 * temp_hex + a
        num += 1
        if num%4 == 0:
            hex_list.append(hex(temp_hex)[2:])
            temp_hex = 0

    final_hex = "".join(map(str,hex_list))

    if i[25] == 0 and i[26] == 1 and i[27] == 1 and i[28] == 0 and i[29] == 1 and i[30] == 1 and i[31] == 1 : # lui opcode = 0110111

        rd = 0
        imm = 0

        for a in i[20:25]:
            rd = rd * 2 + a
        
        if i[0] == 0:
            for a in i[0:20]:
                imm = imm * 2 + a
        else:
            for a in i[0:20]:
                imm = imm * 2 + (1-a)
            imm = -(imm + 1)

       #*******************************왜 하는 지 모르겟음 
        imm = imm * 4096
        #***********************************

        print(f"inst {inst_num}: {final_hex} lui x{rd}, {imm}")
        inst_num +=1

        x[rd] = put_zero_front_hex(imm % pow(2,32))
        # print(s16(int(a,16)))
        # x[rd] = imm % pow(2,32)
    
    elif i[25] == 0 and i[26] == 0 and i[27] == 1 and i[28] == 0 and i[29] == 1 and i[30] == 1 and i[31] == 1 : # auipc 0010111

        rd = 0
        imm = 0

        for a in i[20:25]:
            rd = rd * 2 + a
        
        if i[0] == 0:
            for a in i[0:20]:
                imm = imm * 2 + a
        else:
            for a in i[0:20]:
                imm = imm * 2 + (1-a)
            imm = -(imm + 1)

        imm = imm * 4096

        print(f"inst {inst_num}: {final_hex} auipc x{rd}, {imm}")

        inst_num +=1

    elif i[25] == 1 and i[26] == 1 and i[27] == 0 and i[28] == 1 and i[29] == 1 and i[30] == 1 and i[31] == 1 : # jal 1101111

        rd = 0
        imm = 0

        for a in i[20:25]:
            rd = rd * 2 + a
        
        if i[0] == 0:
            for a in i[12:20]:
                imm = imm * 2 + a
            imm = imm * 2 + i[11]
            for a in i[1:11]:
                imm = imm * 2 + a
        else:
            for a in i[12:20]:
                imm = imm * 2 + (1 - a)
            imm = imm * 2 + (1 - i[11])
            for a in i[1:11]:
                imm = imm * 2 + (1 - a)
            imm = -(imm + 1)
        
        #******************************왜 *2 하는지 모르겠음
        imm = imm * 2
        #******************************왜 *2 하는지 모르겠음

        print(f"inst {inst_num}: {final_hex} jal x{rd}, {imm}")

        inst_num +=1

    elif i[25] == 1 and i[26] == 1 and i[27] == 0 and i[28] == 0 and i[29] == 1 and i[30] == 1 and i[31] == 1 : # jalr 1100111

        rd = 0
        rs1 = 0
        imm = 0

        for a in i[20:25]:
            rd = rd * 2 + a
        
        for a in i[12:17]:
            rs1 = rs1 * 2 + a

        if i[0] == 0:
            for a in i[1:12]:
                imm = imm * 2 + a
        else:
            for a in i[1:12]:
                imm = imm * 2 + (1-a)
            imm = -(imm + 1)

        print(f"inst {inst_num}: {final_hex} jalr x{rd}, {imm}(x{rs1})")

        inst_num +=1

    elif i[25] == 1 and i[26] == 1 and i[27] == 0 and i[28] == 0 and i[29] == 0 and i[30] == 1 and i[31] == 1 : # beq ~ bgeu 1100011

        rs1 = 0
        rs2 = 0
        imm = 0

        for a in i[12:17]:
            rs1 = rs1 * 2 + a

        for a in i[7:12]:
            rs2 = rs2 * 2 + a

        if i[0] == 0:
            imm = imm * 2 + i[24]
            for a in i[1:7]:
                imm = imm * 2 + a
            for a in i[20:25]:
                imm = imm * 2 + a

        else:
            imm = imm * 2 + (1 - i[24])
            for a in i[1:7]:
                imm = imm * 2 + (1-a)
            for a in i[20:25]:
                imm = imm * 2 + (1-a)
            imm = -(imm + 1)

            #*************************왜 또 -1 하는지 모르겠음
            imm = imm - 1
            #*************************왜 또 -1 하는지 모르겠음

        if i[17:20] == [0,0,0]:
            print(f"inst {inst_num}: {final_hex} beq x{rs1}, x{rs2}, {imm}")

        if i[17:20] == [0,0,1]:
            print(f"inst {inst_num}: {final_hex} bne x{rs1}, x{rs2}, {imm}")

        if i[17:20] == [1,0,0]:
            print(f"inst {inst_num}: {final_hex} blt x{rs1}, x{rs2}, {imm}")

        if i[17:20] == [1,0,1]:
            print(f"inst {inst_num}: {final_hex} bge x{rs1}, x{rs2}, {imm}")

        if i[17:20] == [1,1,0]:
            print(f"inst {inst_num}: {final_hex} bltu x{rs1}, x{rs2}, {imm}")

        if i[17:20] == [1,1,1]:
            print(f"inst {inst_num}: {final_hex} bgeu x{rs1}, x{rs2}, {imm}")

        inst_num +=1

    elif i[25] == 0 and i[26] == 0 and i[27] == 0 and i[28] == 0 and i[29] == 0 and i[30] == 1 and i[31] == 1 : # LB ~ lhu 0000011

        rd = 0
        rs1 = 0
        imm = 0

        for a in i[20:25]:
            rd = rd * 2 + a
        
        for a in i[12:17]:
            rs1 = rs1 * 2 + a

        if i[0] == 0:
            for a in i[1:12]:
                imm = imm * 2 + a
        else:
            for a in i[1:12]:
                imm = imm * 2 + (1-a)
            imm = -(imm + 1)

        if i[17:20] == [0,0,0]:
            print(f"inst {inst_num}: {final_hex} lb x{rd}, {imm}(x{rs1})")
        
        if i[17:20] == [0,0,1]:
            print(f"inst {inst_num}: {final_hex} lh x{rd}, {imm}(x{rs1})")

        if i[17:20] == [0,1,0]:
            print(f"inst {inst_num}: {final_hex} lw x{rd}, {imm}(x{rs1})")

        if i[17:20] == [1,0,0]:
            print(f"inst {inst_num}: {final_hex} lbu x{rd}, {imm}(x{rs1})")

        if i[17:20] == [1,0,1]:
            print(f"inst {inst_num}: {final_hex} lhu x{rd}, {imm}(x{rs1})")

        inst_num +=1

    elif i[25] == 0 and i[26] == 1 and i[27] == 0 and i[28] == 0 and i[29] == 0 and i[30] == 1 and i[31] == 1 : # sb ~ sw 0100011

        rs1 = 0
        rs2 = 0
        imm = 0

        for a in i[12:17]:
            rs1 = rs1 * 2 + a

        for a in i[7:12]:
            rs2 = rs2 * 2 + a

        if i[0] == 0:
            for a in i[1:7]:
                imm = imm * 2 + a
            for b in i[20:25]:
                imm = imm * 2 + b

        else:
            for a in i[1:7]:
                imm = imm * 2 + (1-a)
            for b in i[20:25]:
                imm = imm * 2 + (1-b)
            imm = -(imm + 1)

        if i[17:20] == [0,0,0]:
            print(f"inst {inst_num}: {final_hex} sb x{rs2}, {imm}(x{rs1})")

        if i[17:20] == [0,0,1]:
            print(f"inst {inst_num}: {final_hex} sh x{rs2}, {imm}(x{rs1})")

        if i[17:20] == [0,1,0]:
            print(f"inst {inst_num}: {final_hex} sw x{rs2}, {imm}(x{rs1})")

        inst_num +=1

    elif i[25] == 0 and i[26] == 0 and i[27] == 1 and i[28] == 0 and i[29] == 0 and i[30] == 1 and i[31] == 1 : # addi ~ srai 0010011
        rd = 0
        rs1 = 0
        shamt = 0
        imm = 0
        unsigned_imm = 0

        for a in i[20:25]:
            rd = rd * 2 + a
        
        for a in i[12:17]:
            rs1 = rs1 * 2 + a

        for a in i[7:12]:
            shamt = shamt * 2 + a

        if i[0] == 0:
            for a in i[1:12]:
                imm = imm * 2 + a
        else:
            for a in i[1:12]:
                imm = imm * 2 + (1-a)
            imm = -(imm + 1)
        
        for a in i[0:12]:
            unsigned_imm = unsigned_imm * 2 + a

        if i[17:20] == [0,0,1]:
            if i[0:7] == [0,0,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} slli x{rd}, x{rs1}, {shamt}")

                x[rd] = x[rs1] << shamt
                # x[rd] = x[rs1]
                # for j in range(shamt):
                #     x[rd] = x[rd] * 2

        if i[17:20] == [1,0,1]:
            if i[0:7] == [0,0,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} srli x{rd}, x{rs1}, {shamt}")

######################################################
                x[rd] = x[rs1]
                for j in range(shamt):
                    x[rd] = x[rd] / 2

            if i[0:7] == [0,1,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} srai x{rd}, x{rs1}, {shamt}")

                x[rd] = x[rs1]
                for i in range(shamt):
                    x[rd] = x[rd] / 2
                
        if i[17:20] == [0,0,0]:
            print(f"inst {inst_num}: {final_hex} addi x{rd}, x{rs1}, {imm}")

            # x[rd] = x[rs1] + imm
        
        if i[17:20] == [0,1,0]:
            print(f"inst {inst_num}: {final_hex} slti x{rd}, x{rs1}, {imm}")

            if(x[rs1] < imm):
                x[rd] = 1
            else:
                x[rd] = 0

        if i[17:20] == [0,1,1]:
            print(f"inst {inst_num}: {final_hex} sltiu x{rd}, x{rs1}, {imm}")

#######################################
            if(x[rs1] < unsigned_imm):
                x[rd] = 1
            else:
                x[rd] = 0
            ############
            # slti 와 차이 찾기

        if i[17:20] == [1,0,0]:
            print(f"inst {inst_num}: {final_hex} xori x{rd}, x{rs1}, {imm}")

            x[rd] = x[rs1] ^ imm

        if i[17:20] == [1,1,0]:
            print(f"inst {inst_num}: {final_hex} ori x{rd}, x{rs1}, {imm}")

            x[rd] = x[rs1] | imm

        if i[17:20] == [1,1,1]:
            print(f"inst {inst_num}: {final_hex} andi x{rd}, x{rs1}, {imm}")

            x[rd] = x[rs1] & imm

        inst_num +=1

    elif i[25] == 0 and i[26] == 1 and i[27] == 1 and i[28] == 0 and i[29] == 0 and i[30] == 1 and i[31] == 1 : # add ~ and 0110011
        rd = 0
        rs1 = 0
        rs2 = 0

        for a in i[20:25]:
            rd = rd * 2 + a
        
        for a in i[12:17]:
            rs1 = rs1 * 2 + a
        
        for a in i[7:12]:
            rs2 = rs2 * 2 + a


        if i[17:20] == [0,0,0]:
            if i[0:7] == [0,0,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} add x{rd}, x{rs1}, x{rs2}")

                x[rd] = x[rs1] + x[rs2]

            if i[0:7] == [0,1,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} sub x{rd}, x{rs1}, x{rs2}")

                x[rd] = x[rs1] - x[rs2]

        if i[17:20] == [0,0,1]:
            if i[0:7] == [0,0,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} sll x{rd}, x{rs1}, x{rs2}")

                x[rd] = x[rs1] * pow(2, x[rs2])

        if i[17:20] == [0,1,0]:
            if i[0:7] == [0,0,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} slt x{rd}, x{rs1}, x{rs2}")


                if(x[rs1] < x[rs2]):
                    x[rd] = 1
                else:
                    x[rd] = 0

        if i[17:20] == [0,1,1]:
            if i[0:7] == [0,0,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} sltu x{rd}, x{rs1}, x{rs2}")

        if i[17:20] == [1,0,0]:
            if i[0:7] == [0,0,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} xor x{rd}, x{rs1}, x{rs2}")

                x[rd] = x[rs1] ^ x[rs2]

        if i[17:20] == [1,0,1]:
            if i[0:7] == [0,0,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} srl x{rd}, x{rs1}, x{rs2}")

                x[rd] = x[rs1] / (pow(2,x[rs2]))

            if i[0:7] == [0,1,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} sra x{rd}, x{rs1}, x{rs2}")
############################################
                x[rd] = x[rs1] / (pow(2,x[rs2]))

        if i[17:20] == [1,1,0]:
            if i[0:7] == [0,0,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} or x{rd}, x{rs1}, x{rs2}")

                x[rd] = x[rs1] | x[rs2]

        if i[17:20] == [1,1,1]:
            if i[0:7] == [0,0,0,0,0,0,0]:
                print(f"inst {inst_num}: {final_hex} and x{rd}, x{rs1}, x{rs2}")

                x[rd] = x[rs1] & x[rs2]
        inst_num +=1


    else:
        print(f"inst {inst_num}: {final_hex} unknown instruction")
        inst_num +=1

x[0] = 0

for i in range(32):
    print(f"x{i}: {x[i]}")