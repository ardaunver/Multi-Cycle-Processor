import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from cocotb.triggers import RisingEdge
from cocotb.binary import BinaryValue

def print_wires(dut):
    print(' Wires:\n')
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
async def ISA_TEST(dut):

    num_cycle = 5

    """Setup testbench and run a test."""

    # Generate the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))

    # set clkedge as the falling edge for triggers
    clkedge = RisingEdge(dut.clk)

    # wait until the falling edge
    dut.reset.value = 1
    await clkedge

    print("\n### TESTING ISAs ###")
    print("-----------------------------------------")

    dut.state_out.value = 0
    dut.reset.value = 0

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

    # LDR R3, [R0, #104];
    # E4103068

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 10

    print("### End of instruction ###\n")

    # ADD R4, R2, R3;
    # E0824003

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 19
   
    print("### End of instruction ###\n")

    print("Registers:\nR2 <-- 9\nR3 <-- 10\nR4 <-- R2 + R3 = 19\n")


    # SUB R1, R3, R2;
    # E0431002

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 1
   
    print("### End of instruction ###\n")

    print("Registers:\nR1 <-- 1\nR2 <-- 9\nR3 <-- 10\nR4 <-- 19\n")


    # ORR R6, R2, R3;
    # E1826003 
    
    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 11
   
    print("### End of instruction ###\n")


    
    # AND R5, R2, R3;
    # E0025003

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 8
   
    print("### End of instruction ###\n")

    print("Registers:\nR1 <-- 1\nR2 <-- 9\nR3 <-- 10\nR4 <-- 19\nR5 <-- 8\nR6 <-- 11\n")


    # MOV R7, R1, #2; (R7 <-- R1 * 2^2 = 4)
    # E1A07101

    # 1110 00 0 1101 0 0000 0111 00010 00 0 0001 
    #      ^DP  ^MOVE        ^Rd       ^LSL  ^Rm

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 4

    print("### End of instruction ###\n")

    print("Registers:\nR1 <-- 1\nR2 <-- 9\nR3 <-- 10\nR4 <-- 19\nR5 <-- 8\nR6 <-- 11\nR7 <-- 4\n")

    

    # Line 29 in mem_data

    # STR R7, R0, #96; 
    # E4007060

    # 1110 01 000000 0000 0111 000001100000  
    #      ^MEM ^STR  ^Rn  ^Rd     ^imm12

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0


    print("### End of instruction ###\n")

    # Line 33 in mem_data

    # LDR R8, [R0, #96];
    # E4108060

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 4

    print("### End of instruction ###\n")

    print("Registers:\nR1 <-- 1\nR2 <-- 9\nR3 <-- 10\nR4 <-- 19\nR5 <-- 8\nR6 <-- 11\nR7 <-- 4\nR8 <-- 4\n")

    # CMP R2, R6, R5;
    # E1462005

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RegWrite_out.value == 0
    print("CMP operation did not change the values written in registers.\n")

    print("### End of instruction ###\n")

    # BEQ 80;
    # 08000014

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    print("### End of instruction ###\n")

    # CMP R8, R7, R7;
    # E1487007

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.z_out.value == 1
    print("CMP operation set the Z flag to 1\n")

    print("Registers:\nR1 <-- 1\nR2 <-- 9\nR3 <-- 10\nR4 <-- 19\nR5 <-- 8\nR6 <-- 11\nR7 <-- 4\nR8 <-- 4\n")

    # BEQ 80;
    # 08000014

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 80
    print("### End of instruction ###\n")


    # ADD R8, R8, R1;
    # E0888001

    for i in range(num_cycle):

        await clkedge
        print("[Cycle ", i+1, "]\n")
        print_wires(dut)
        print_ctrl_signals(dut)
        dut.reset.value = 0

    assert dut.RESULT.value == 5
   
    print("### End of instruction ###\n")

    print("Registers:\nR1 <-- 1\nR2 <-- 9\nR3 <-- 10\nR4 <-- 19\nR5 <-- 8\nR6 <-- 11\nR7 <-- 4\nR8 <-- 5\n")



    


    


    


    
    

    