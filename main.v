module main( input clk, 
				 input reset,
				 output [2:0] state_out,
				 output [31:0] RESULT, PC
				);

wire [3:0] cond_out;
wire [1:0] op_out;
wire [5:0] funct_out;
wire [3:0] rd_out;

wire z_out;

wire PCWrite_out;
wire AdrSrc_out;
wire MemWrite_out;
wire IRWrite_out;

wire Z_enable_out;
wire BLenable_out;
wire Bxenable_out;
  
wire RegWrite_out;
wire [1:0] ImmSrc_out;
wire [1:0] RegSrc_out;
wire ALUSrcA_out;
wire [1:0] ALUSrcB_out;
wire [3:0] ALUControl_out;
wire [1:0] ResultSrc_out;



wire [3:0] RA1, RA2, A3;
wire [31:0] RD1, RD2, SrcA, SrcB, ExtImm;
wire [31:0] ALU_OUT, A, Data, INSTR;

DATAPATH #(.WIDTH(32)) DP
    (
	  .clk(clk), .reset(reset),
	  
	  // Control Signals
	  .PCWrite(PCWrite_out), .AdrSrc(AdrSrc_out), .MemWrite(MemWrite_out), .IRWrite(IRWrite_out), .RegWrite(RegWrite_out), .ALUSrcA(ALUSrcA_out),
	  .RegSrc(RegSrc_out), .ImmSrc(ImmSrc_out), .ALUSrcB(ALUSrcB_out), .ResultSrc(ResultSrc_out), .Z_enable(Z_enable_out), .BLenable(BLenable_out), .BXenable(Bxenable_out),
	  .ALUControl(ALUControl_out),
	  
	  // Output signals
	  .Cond(cond_out),
	  .Op(op_out),
	  .Funct(funct_out),
	  .Rd(rd_out),
	  
	  .RA1(RA1), .RA2(RA2), .A3(A3),
	  .RD1(RD1), .RD2(RD2), .PC(PC), .RESULT(RESULT),
	  .ALU_OUT(ALU_OUT), .A(A), .Data(Data), .INSTR(INSTR), .SrcA(SrcA), .SrcB(SrcB), .ExtImm(ExtImm),
	  
	  .Z(z_out)
	  
    );
	 
CONTROLLER CTRL 
    (
	  .clk(clk),
	  .Cond(cond_out),
	  .Op(op_out),
	  .Funct(funct_out),
	  .Rd(rd_out),
	  
	  .Z(z_out),
	  .Z_enable(Z_enable_out),
	  .PCWrite(PCWrite_out),
	  .AdrSrc(AdrSrc_out),
	  .MemWrite(MemWrite_out),
	  .IRWrite(IRWrite_out),
	  
	  .BLenable(BLenable_out),
	  .BXenable(Bxenable_out),
	  
	  .RegWrite(RegWrite_out),
	  .ImmSrc(ImmSrc_out),
	  .RegSrc(RegSrc_out),
	  .ALUSrcA(ALUSrcA_out),
	  .ALUSrcB(ALUSrcB_out),
	  .ALUControl(ALUControl_out),
	  .ResultSrc(ResultSrc_out),
	  .state(state_out)
	  
    );

endmodule 