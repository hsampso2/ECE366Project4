# Authors: Henry Sampson, Seyda Ali
# add, sub, xor, addi, beq, bne, slt, lw, sw
# -----------------------------------------------------------

print("ECE366 Fall 2018 mini MIPS compiler")
input_file = open("A1.txt", "r")
output_file = open("memory.txt", "w")
register = []  # registers

i = 0
while i < 8:  # allocate 8 registers
    register.append(0)
    i = i + 1

imm = 0  # second argument (immediate)

instruction_Count = 0
Cycle = 1
threeCycles = 0
fourCycles = 0
fiveCycles = 0

instruction_Memory = []  # create instruction memory
pattern = [] #data from patterns

i = 0;
while i < (12288):  # allocate data memory space
    instruction_Memory.append(0)
    i = i + 1
for line in input_file:
    pattern.append(line)
i = 0
while i < len(pattern):
    instruction_Memory[i] = format(int(pattern[i], 16), "032b")
    i = i + 1
i = 0 #PC
while i < 4096:
    print("Instruction Line " + str(i) + ": " + "R[0]->" + str(register[0]) + " " + "R[1]->" + str(register[1]) + " " + "R[2]->" + str(register[2]) + " " + "R[3]->" + str(register[3]) + "\n")
    if (instruction_Memory[i][0:6] == '000000' and instruction_Memory[i][26:32] == '100000'):  # add
        Cycle += 4
        fourCycles += 1
        register[int(instruction_Memory[i][16:21], 2)] = register[int(instruction_Memory[i][6:11], 2)] + register[int(instruction_Memory[i][11:16], 2)]

    elif (instruction_Memory[i][0:6] == '000000' and instruction_Memory[i][26:32] == '100010'):  # sub
        Cycle += 4
        fourCycles += 1
        register[int(instruction_Memory[i][16:21], 2)] = register[int(instruction_Memory[i][6:11], 2)] - register[int(instruction_Memory[i][11:16], 2)]

    elif (instruction_Memory[i][0:6] == '000000' and instruction_Memory[i][26:32] == '100110'):  # xor
        Cycle += 4
        fourCycles += 1
        register[int(instruction_Memory[i][16:21], 2)] = register[int(instruction_Memory[i][6:11], 2)] ^ register[int(instruction_Memory[i][11:16], 2)]

    elif (instruction_Memory[i][0:6] == '001000'):  # addi
        Cycle += 4
        fourCycles += 1
        imm = int(instruction_Memory[i][16:32], 2) if instruction_Memory[i][16] == '0' else -(65535 - int(instruction_Memory[i][16:32], 2) + 1)
        register[int(instruction_Memory[i][11:16], 2)] = register[int(instruction_Memory[i][6:11], 2)] + imm

    elif (instruction_Memory[i][0:6] == '000100'):  # beq
        Cycle += 3
        threeCycles += 1
        imm = int(instruction_Memory[i][16:32], 2) if instruction_Memory[i][16] == '0' else -(65535 - int(instruction_Memory[i][16:32], 2) + 1)
        i = i + imm - 1 if (register[int(instruction_Memory[i][6:11], 2)] == register[int(instruction_Memory[i][11:16], 2)]) else i

    elif (instruction_Memory[i][0:6] == '000101'):  # bne
        Cycle += 3
        threeCycles += 1
        imm = int(instruction_Memory[i][16:32], 2) if instruction_Memory[i][16] == '0' else -(65535 - int(instruction_Memory[i][16:32], 2) + 1)
        i = i + imm - 1 if (register[int(instruction_Memory[i][6:11], 2)] != register[int(instruction_Memory[i][11:16], 2)]) else i

    elif (instruction_Memory[i][0:6] == '000000' and instruction_Memory[i][26:32] == '101010'):  # slt
        Cycle += 4
        fourCycles += 1
        register[int(instruction_Memory[i][16:21], 2)] = 1 if register[int(instruction_Memory[i][6:11], 2)] < register[int(instruction_Memory[i][11:16], 2)] else 0

    elif (instruction_Memory[i][0:6] == '101011'):  # sw
        Cycle += 4
        fourCycles += 1
        imm = int(instruction_Memory[i][16:32], 2)
        instruction_Memory[imm + register[int(instruction_Memory[i][6:11], 2)] - 8192] = register[int(instruction_Memory[i][11:16], 2)]  # Store word into memory

    elif (instruction_Memory[i][1:4] == '110'):  # lw
        Cycle += 5
        fiveCycles += 1
        imm = int(instruction_Memory[i][16:32], 2)
        register[int(instruction_Memory[i][11:16], 2)] = instruction_Memory[imm + register[int(instruction_Memory[i][6:11], 2)] - 8192]  # Load memory into register

    elif (instruction_Memory[i][0:32] == '00010000000000001111111111111111'):
        break

    else:
        instruction_Count = instruction_Count - 1

    instruction_Count = instruction_Count + 1
    i = i + 1
print("Instruction Line " + str(i) + ": " + "R[0]->" + str(register[0]) + " " + "R[1]->" + str(register[1]) + " " + "R[2]->" + str(register[2]) + " " + "R[3]->" + str(register[3]) + "\n")
output_file.write("Instruction Count: " + str(instruction_Count) + "\n" + "\n")
output_file.write("Cycles: " + str(Cycle) + "\n" + "\n")
output_file.write("3 Cycle: " + str(threeCycles) + "\n" + "\n")
output_file.write("4 Cycle: " + str(fourCycles) + "\n" + "\n")
output_file.write("5 Cycle: " + str(fiveCycles) + "\n" + "\n")
i = 0
for x in register:
    output_file.write("Register " + str(i) + ": " + str(x) + "\n")
    i = i + 1
output_file.write("\n")
i = 0
for x in instruction_Memory:
    output_file.write("Address " + str(i) + ": " + str(x) + "\n")
    i = i + 1

input_file.close()
output_file.close()
