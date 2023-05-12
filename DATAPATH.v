module DATAPATH #(parameter WIDTH = 32)
    (
	  input clk, reset,
	  
	  // Control Signals
	  input PCWrite, AdrSrc, MemWrite, IRWrite, RegWrite, ALUSrcA, Z_enable, BLenable, BXenable,
	  input [1:0] RegSrc, ImmSrc, ALUSrcB, ResultSrc,
	  input [3:0] ALUControl,
	  
	  // Output signals
	  output [3:0] Cond,
	  output [1:0] Op,
	  output [5:0] Funct,
	  output [3:0] Rd,
	  
	  output [3:0] RA1, RA2, A3,
	  output [WIDTH-1:0] RD1, RD2, PC, RESULT, 
	  output [WIDTH-1:0] ALU_OUT, A, Data, INSTR, SrcA, SrcB, ExtImm,
	  output Z
    );
	 
	 
wire [WIDTH-1 : 0] Adr, WriteData, ReadData, ALU_RESULT, ShiftOut;

wire zero, ZRegInput;

wire [3:0] preRA1;
	 
	 
Register_sync_rw #(.WIDTH(WIDTH)) PC_reg (.clk(clk), .reset(reset), .we(PCWrite), .DATA(RESULT), .OUT(PC));

Register_sync_rw #(.WIDTH(WIDTH)) INSTR_reg (.clk(clk), .reset(reset), .we(IRWrite) , .DATA(ReadData), .OUT(INSTR));
	 
Data_memory InstrData (.clk(clk), .WE(MemWrite), .ADDR(Adr), .WD(WriteData), .RD(ReadData));

Mux_2to1 #(.WIDTH(WIDTH)) ADDRESS (.select(AdrSrc), .input_0(PC), .input_1(RESULT), .output_value(Adr));

Mux_2to1 regsrc0 (.select(RegSrc[0]), .input_0(INSTR[19:16]), .input_1(15), .output_value(preRA1));

Mux_2to1 regsrc1 (.select(RegSrc[1]), .input_0(INSTR[3:0]), .input_1(INSTR[15:12]), .output_value(RA2));

Register_simple #(.WIDTH(WIDTH)) Data_reg (.clk(clk), .reset(reset), .DATA(ReadData), .OUT(Data));

Extender Ext (.A(INSTR[23:0]), .select(ImmSrc), .Q(ExtImm));

Register_file #(.WIDTH(WIDTH)) RegF (.clk(clk), .write_enable(RegWrite), .reset(reset), 
												.Source_select_0(RA1), .Source_select_1(RA2), .Destination_select(A3), 
												.DATA(RESULT), .Reg_15(RESULT), 
												.out_0(RD1), .out_1(RD2));
												
Double_Register_simple  #(.WIDTH(WIDTH)) D_reg (.clk(clk), .reset(reset), .DATA1(RD1), .DATA2(RD2), .OUT1(A), .OUT2(WriteData));

shifter #(.WIDTH(WIDTH)) SHIFT (.control(INSTR[6:5]), .shamt(INSTR[11:7]), .DATA(WriteData), .OUT(ShiftOut));

Mux_4to1 #(.WIDTH(WIDTH)) SrcB_reg (.select(ALUSrcB), .input_0(ShiftOut), .input_1(ExtImm), .input_2(4), .input_3(0), .output_value(SrcB));

Mux_2to1 #(.WIDTH(WIDTH)) BeforeAlu (.select(ALUSrcA), .input_0(A), .input_1(PC), .output_value(SrcA));

ALU #(.WIDTH(WIDTH)) ALU (.control(ALUControl), .CI(0), .DATA_A(SrcA), .DATA_B(SrcB), .OUT(ALU_RESULT), .CO(zero), .OVF(zero), .N(zero), .Z(ZRegInput));

Register_sync_rw #(.WIDTH(WIDTH)) RegZ (.clk(clk), .reset(reset), .we(Z_enable) , .DATA(ZRegInput), .OUT(Z));

Register_simple #(.WIDTH(WIDTH)) ALU_reg (.clk(clk), .reset(reset), .DATA(ALU_RESULT), .OUT(ALU_OUT));

Mux_4to1 #(.WIDTH(WIDTH)) Result_reg (.select(ResultSrc), .input_0(ALU_OUT), .input_1(Data), .input_2(ALU_RESULT), .input_3(0), .output_value(RESULT));


Mux_2to1 BLreg (.select(BLenable), .input_0(INSTR[15:12]), .input_1(14), .output_value(A3)); // If BLenable is 1, Destination is R14

Mux_2to1 BXreg (.select(BXenable), .input_0(preRA1), .input_1(14), .output_value(RA1));
		

// Inputs for the Controller
assign Cond = INSTR[31:28];
assign Op = INSTR[27:26];
assign Funct = INSTR[25:20];
assign Rd = INSTR[15:12];
		
endmodule
