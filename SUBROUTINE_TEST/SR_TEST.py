import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from cocotb.triggers import RisingEdge
from cocotb.binary import BinaryValue

def print_wires(dut):
    print('Wires:\n')
    print(f'PC: {dut.PC.value}')
    print(f'State: {dut.state_out.value}')
    print(f'INSTR: {dut.INSTR.value}')
    print('-----')
    print(f'RA1: {dut.RA1.value}')
    print(f'RA2: {dut.RA2.value}')
    print('-----')
    print(f'RD1: {dut.RD1.value}')
    print(f'RD2: {dut.RD2.value}')
    print('-----')
    print(f'SrcA: {dut.SrcA.value}')
    print(f'SrcB: {dut.SrcB.value}')
    print(f'ExtImm: {dut.ExtImm.value}')
    print('-----')
    print(f'ALU OUT: {dut.ALU_OUT.value}')
    print('-----')
    print(f'RESULT: {dut.RESULT.value}\n')

def print_ctrl_signals(dut):
    print('Control Signals:\n')
    print(f'PCWrite: {dut.PCWrite_out.value}')
    print(f'AdrSrc: {dut.AdrSrc_out.value}')
    print(f'MemWrite: {dut.MemWrite_out.value}')
    print(f'IRWrite: {dut.IRWrite_out.value}')
    print(f'RegWrite: {dut.RegWrite_out.value}')
    print(f'ImmSrc: {dut.ImmSrc_out.value}')
    print(f'RegSrc: {dut.RegSrc_out.value}')
    print(f'ALUSrcA: {dut.ALUSrcA_out.value}')
    print(f'ALUSrcB: {dut.ALUSrcB_out.value}')
    print(f'ALUControl: {dut.ALUControl_out.value}')
    print(f'ResultSrc: {dut.ResultSrc_out.value}')
    print(f'Flag Z: {dut.z_out.value}\n')
    print(f'ENABLE Z: {dut.Z_enable_out.value}\n')



@cocotb.test()
async def SR_TEST(dut):

    num_cycle = 5

    """Setup testbench and run a test."""

    # Generate the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))

    # set clkedge as the falling edge for triggers
    clkedge = RisingEdge(dut.clk)

    # wait until the falling edge
    dut.reset.value = 1
    await clkedge

    print("\n### TESTING SUBROUTINES ###")
    print("-----------------------------------------")

    dut.state_out.value = 0
    dut.reset.value = 0


    print("TESTING 2'S COMPLEMENT SUBROUTINE...\n")

    print("COMPUTING 2'S COMPLEMENT OF 9")
    print("DESIRED OUTPUT: FFFFFFF7\n")

    # LDR R2, [R1, #100];
    # E4112064

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 9

    print("### End of instruction ###\n")

    print("Registers:\nR2 <-- 0000 0009\n")

    # B 40;
    # E800000A

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 40
    print("### End of instruction ###\n")

    print("Branch to 40 where 2's complement subroutine is located.\n")


    # SUB R2, R1, R2;
    # E0412002

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 0b11111111111111111111111111110111

    print("Registers:\nR2 <-- FFFF FFF7\n")
   
    print("### End of instruction ###\n")

    # B 8;
    # E8000002

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 8
    print("### End of instruction ###\n")

    print("Exiting the subroutine...\n")

    print("Branching back to 8...\n")

    # LDR R3, [R1, #104];
    # E4113068

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 3

    print("### End of instruction ###\n")

    print("Registers:\nR2 <-- F7\nR3 <-- 3\n")

    # LDR R4, [R1, #108];
    # E411406C

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 4

    print("### End of instruction ###\n")

    print("Registers:\nR2 <-- F7\nR3 <-- 3\nR4 <-- 4\n")

    # LDR R1, [R0, #112];
    # E4101070

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 1

    print("### End of instruction ###\n")

    print("Registers:\nR1 <-- 1\nR2 <-- F7\nR3 <-- 3\nR4 <-- 4\n")

    # LDR R5, [R0, #116];
    # E4105074

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 120

    print("### End of instruction ###\n")

    print("Registers:\nR1 <-- 1 (subtract 1 at each loop)\nR2 <-- F7")
    print("R3 <-- 3 (number of loops)\nR4 <-- 4 (address offset)\nR5 <-- 120 (base address)\n")

    # B 64;
    # E8000010

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 64
    print("### End of instruction ###\n")

    print("Branch to 64 where Sum of Array subroutine is located.\n")

    print("COMPUTING SUM OF AN ARRAY...\n")

    print("DESIRED OUTPUT:\n")

    print("   (HEX) (DEC)")
    print("     1A   26")
    print("     2B   43")
    print("     3C   60")
    print("   +    +")
    print("   ---- -----")
    print("     81   129\n")

    # LDR R6, [R5];
    # E4156000

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 26

    print("### End of instruction ###\n")


    # ADD R10, R10, R6;
    # E08AA006

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 26
   
    print("### End of instruction ###\n")

    # SUB R3, R3, R1;
    # E0433001

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 2
   
    print("### End of instruction ###\n")

    # CMP R3, R3, R0;
    # E1433000

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RegWrite_out.value == 0
    assert dut.RESULT.value == 2
    print("CMP operation did not change the values written in registers.\n")

    print("### End of instruction ###\n")

    # BEQ 28;
    # 08000007

    # Branch to 28 if the subroutine ends

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    print("### End of instruction ###\n")

    print("Flag Z is not set. Continue the loop.")

    # ADD R5, R5, R4;
    # E0855004

    # Increment the base address [R5] by 4 

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 124
   
    print("### End of instruction ###\n")

    # B 64;
    # E8000010

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 64
    print("### End of instruction ###\n")

    print("Branch to 64 where Sum of Array subroutine is located.\n")




    
    print("#############################")
    print("#### GO FOR ANOTHER LOOP ####")
    print("#############################")







    # LDR R6, [R5];
    # E4156000

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 43

    print("### End of instruction ###\n")


    # ADD R10, R10, R6;
    # E08AA006

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 69
   
    print("### End of instruction ###\n")

    # SUB R3, R3, R1;
    # E0433001

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 1
   
    print("### End of instruction ###\n")

    # CMP R3, R3, R0;
    # E1433000

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RegWrite_out.value == 0
    assert dut.RESULT.value == 1
    print("CMP operation did not change the values written in registers.\n")

    print("### End of instruction ###\n")

    # BEQ 28;
    # 08000007

    # Branch to 28 if the subroutine ends

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    print("### End of instruction ###\n")

    print("Flag Z is not set. Continue the loop.")

    # ADD R5, R5, R4;
    # E0855004

    # Increment the base address [R5] by 4 

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 128
   
    print("### End of instruction ###\n")

    # B 64;
    # E8000010

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 64
    print("### End of instruction ###\n")

    print("Branch to 64 where Sum of Array subroutine is located.\n")




    print("#############################")
    print("#### GO FOR ANOTHER LOOP ####")
    print("#############################")







    # LDR R6, [R5];
    # E4156000

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 60

    print("### End of instruction ###\n")


    # ADD R10, R10, R6;
    # E08AA006

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 129
   
    print("### End of instruction ###\n")

    # SUB R3, R3, R1;
    # E0433001

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 0
   
    print("### End of instruction ###\n")

    # CMP R3, R3, R0;
    # E1433000

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RegWrite_out.value == 0
    assert dut.RESULT.value == 0
    print("CMP operation did not change the values written in registers.\n")

    print("### End of instruction ###\n")

    # BEQ 28;
    # 08000007

    # Branch to 28 if the subroutine ends

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    print("### End of instruction ###\n")

    print("Flag Z is now set.\n")

    print("Exiting the Sum of Array subroutine...\n")

    print("Branching back to 28...\n")


    print("Registers:\nR1 <-- 1\nR2 <-- FFFF FFF7 (2's Complement of 9)")
    print("R3 <-- 0\nR4 <-- 4\nR5 <-- 128\nR6 <-- 60\nR10 <-- 0000 003C (129)\n")


    # LDR R9, [R3, #120];
    # E4139078

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 26

    print("### End of instruction ###\n")


    # B 132;
    # E8000021

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 132
    print("### End of instruction ###\n")

    print("Branch to 132 where Even Parity Check subroutine is located.\n")

    print("COMPUTING EVEN PARITY CHECK...\n")

    print("INPUT: 0001 1010 (26)\n")

    print("DESIRED OUTPUT: 1")
    print("Since number of ones in binary number 26 is odd.\n")

    print("*** will be used")

    print("Registers:\nR1 <-- 1 ***\nR2 <-- FFFF FFF7")
    print("R3 <-- 0\nR4 <-- 4\nR5 <-- 128\nR6 <-- 60\nR9 <-- 26 *** (INPUT)\nR10 <-- 0000 003C (129)\n")

    print("R8 will count the number of ones")


    # CMP R9, R9, R3;
    # E1499003

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RegWrite_out.value == 0
    print("CMP operation did not change the values written in registers.\n")

    print("### End of instruction ###\n")

    # BEQ 160;
    # 08000028

    # Branch to 160 if the number is 0

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    print("### End of instruction ###\n")

    print("Flag Z is not set. Continue the loop.")


    # AND R0, R9, R1;
    # E0090001

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 0
   
    print("### End of instruction ###\n")


    # ADD R8, R8, R0;
    # E0888000


    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 0
   
    print("### End of instruction ###\n")


    # MOV R9, R9, #1; 
    # E1A090A9

    # 1110 00 0 1101 0 0000 1001 00001 01 0 9001 
    #      ^DP  ^MOVE        ^Rd       ^LSR  ^Rm

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 13

    print("### End of instruction ###\n")

    # B 132;
    # E8000021

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0


    print("Branch to 132 where Even Parity Check subroutine is located.\n")
 
    print("#############################")
    print("#### GO FOR ANOTHER LOOP ####")
    print("#############################\n")


    # CMP R9, R9, R3;
    # E1499003

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RegWrite_out.value == 0
    print("CMP operation did not change the values written in registers.\n")

    print("### End of instruction ###\n")

    # BEQ 160;
    # 08000028

    # Branch to 160 if the number is 0

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    print("### End of instruction ###\n")

    print("Flag Z is not set. Continue the loop.")


    # AND R0, R9, R1;
    # E0090001

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 1
   
    print("### End of instruction ###\n")


    # ADD R8, R8, R0;
    # E0888000


    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 1
   
    print("### End of instruction ###\n")


    # MOV R9, R9, #1; 
    # E1A090A9

    # 1110 00 0 1101 0 0000 1001 00001 01 0 9001 
    #      ^DP  ^MOVE        ^Rd       ^LSR  ^Rm

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 6

    print("### End of instruction ###\n")

    # B 132;
    # E8000021

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0


    print("Branch to 132 where Even Parity Check subroutine is located.\n")
 
    print("#############################")
    print("#### GO FOR ANOTHER LOOP ####")
    print("#############################\n")


    # CMP R9, R9, R3;
    # E1499003

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RegWrite_out.value == 0
    print("CMP operation did not change the values written in registers.\n")

    print("### End of instruction ###\n")

    # BEQ 160;
    # 08000028

    # Branch to 160 if the number is 0

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    print("### End of instruction ###\n")

    print("Flag Z is not set. Continue the loop.")


    # AND R0, R9, R1;
    # E0090001

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 0 
   
    print("### End of instruction ###\n")


    # ADD R8, R8, R0;
    # E0888000


    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 1
   
    print("### End of instruction ###\n")


    # MOV R9, R9, #1; 
    # E1A090A9

    # 1110 00 0 1101 0 0000 1001 00001 01 0 9001 
    #      ^DP  ^MOVE        ^Rd       ^LSR  ^Rm

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 3

    print("### End of instruction ###\n")

    # B 132;
    # E8000021

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0


    print("Branch to 132 where Even Parity Check subroutine is located.\n")
 
    print("#############################")
    print("#### GO FOR ANOTHER LOOP ####")
    print("#############################\n")


    # CMP R9, R9, R3;
    # E1499003

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RegWrite_out.value == 0
    print("CMP operation did not change the values written in registers.\n")

    print("### End of instruction ###\n")

    # BEQ 160;
    # 08000028

    # Branch to 160 if the number is 0

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    print("### End of instruction ###\n")

    print("Flag Z is not set. Continue the loop.")


    # AND R0, R9, R1;
    # E0090001

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 1 
   
    print("### End of instruction ###\n")


    # ADD R8, R8, R0;
    # E0888000


    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 2
   
    print("### End of instruction ###\n")


    # MOV R9, R9, #1; 
    # E1A090A9

    # 1110 00 0 1101 0 0000 1001 00001 01 0 9001 
    #      ^DP  ^MOVE        ^Rd       ^LSR  ^Rm

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 1

    print("### End of instruction ###\n")

    # B 132;
    # E8000021

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0


    print("Branch to 132 where Even Parity Check subroutine is located.\n")
 
    print("#############################")
    print("#### GO FOR ANOTHER LOOP ####")
    print("#############################\n")


    # CMP R9, R9, R3;
    # E1499003

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RegWrite_out.value == 0
    print("CMP operation did not change the values written in registers.\n")

    print("### End of instruction ###\n")

    # BEQ 160;
    # 08000028

    # Branch to 160 if the number is 0

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    print("### End of instruction ###\n")

    print("Flag Z is not set. Continue the loop.")


    # AND R0, R9, R1;
    # E0090001

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 1 
   
    print("### End of instruction ###\n")


    # ADD R8, R8, R0;
    # E0888000


    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 3
   
    print("### End of instruction ###\n")


    # MOV R9, R9, #1; 
    # E1A090A9

    # 1110 00 0 1101 0 0000 1001 00001 01 0 9001 
    #      ^DP  ^MOVE        ^Rd       ^LSR  ^Rm

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 0

    print("### End of instruction ###\n")

    # B 132;
    # E8000021

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0


    print("Branch to 132 where Even Parity Check subroutine is located.\n")
 
    print("#############################")
    print("#### GO FOR ANOTHER LOOP ####")
    print("#############################\n")


    # CMP R9, R9, R3;
    # E1499003

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RegWrite_out.value == 0
    print("CMP operation set te Flag Z\n")

    print("### End of instruction ###\n")

    # BEQ 160;
    # 08000028

    # Branch to 160 if the number is 0

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    print("### End of instruction ###\n")

    print("Flag Z is not set. Continue the loop.")


    # AND R0, R8, R1;
    # E0080001

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 1 
   
    print("### End of instruction ###\n")


    print("1 is written in R0, meaning that the number of ones in binary number 26 is odd.\n")

    print("Exitting the Even Parity Check Subroutine...\n")

    print("Branching back to 0 \n")


    # B 0;
    # E8000000

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0





    