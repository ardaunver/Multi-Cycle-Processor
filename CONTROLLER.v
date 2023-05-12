module CONTROLLER 
    (
	  input clk,
	  input [3:0] Cond,
	  input [1:0] Op,
	  input [5:0] Funct,
	  input [3:0] Rd,
	  
	  input  Z,
	  
	  output reg Z_enable,
	  output reg BLenable,
	  output reg BXenable,
	  
	  output reg PCWrite,
	  output reg AdrSrc,
	  output reg MemWrite,
	  output reg IRWrite,
	  
	  output reg RegWrite,
	  output reg [1:0] ImmSrc,
	  output reg [1:0] RegSrc,
	  output reg ALUSrcA,
	  output reg [1:0] ALUSrcB,
	  output reg [3:0] ALUControl,
	  output reg [1:0] ResultSrc,
	  output reg [2:0] state
	  
    );
	 
reg CondEx;

	
	 
always @(posedge clk) begin

if(state == 4)
	state = 0;
	
else
	state = state + 1;
	

end


//Conditional Logic (clock)
always @(*) begin

	case(Cond)
	
		4'b0000: // EQ
					if(Z == 1)
						CondEx = 1;
					else
						CondEx = 0;
		
		4'b0001:	// NE
					if(Z == 0)
						CondEx = 1;
					else 
						CondEx = 0;
		
		4'b1110:  // AL
					CondEx = 1;
		
		default: CondEx = 1;
					
		
endcase	

end 


always @(*) begin

	
if(state == 0) begin 

	// Fetch Cycle (Cycle 1)

	PCWrite 		= 1'b1;
	AdrSrc   	= 1'b0;
	MemWrite 	= 1'b0;
	IRWrite  	= 1'b1;
	
	RegSrc 		= 2'b00; // don't care (not decoded yet)
		  
	RegWrite 	= 1'b0;
	ImmSrc   	= 2'b00; // don't care
	ALUSrcA  	= 1'b1;
	ALUSrcB  	= 2'b10;
	ALUControl 	= 4'b0100; // ADD
	ResultSrc 	= 2'b10;
	
	Z_enable = 1'b0; // Don't change Z flag in FETCH
	
	BLenable = 1'b0;
	BXenable = 1'b0;
	
	
	end

if(state == 1) begin 
	
	// Decode Cycle (Cycle 2)

	PCWrite 		= 1'b0; // !
	AdrSrc   	= 1'b0; // don't care
	MemWrite 	= 1'b0;
	IRWrite  	= 1'b0; // !
	
	case(Op)
	
		2'b00: RegSrc		= 2'b00;
		
		2'b01: RegSrc		= 2'b10; 
			 // RegSrc		= {~Funct[0], 1'b0};

		2'b10: RegSrc		= 2'b00;
		
		default: RegSrc		= 2'b00;

	endcase  
	
	RegWrite 	= 1'b0;
	ImmSrc   	= {Op}; // don't care
	ALUSrcA  	= 1'b1;
	ALUSrcB  	= 2'b10;
	ALUControl 	= 4'b0100; // ADD
	ResultSrc 	= 2'b10;
	
	Z_enable = 1'b0; // Don't change Z flag in DECODE
	
	if((Op == 2'b10) && ({Funct[5:4]} == 2'b10)) 
		BLenable = 1'b1;
	else
		BLenable = 1'b0;
	if((Op == 2'b10) && ({Funct[5:4]} == 2'b11)) 
		BXenable = 1'b1;
	else
		BXenable = 1'b0;
		
	
	end
	
else if(state == 2) begin 

	case(Op)
		
		// Memory Instruction
		2'b01: // MemAddr Cycle (Cycle 3)
			begin
				
			PCWrite 		= 1'b0; 
			AdrSrc   	= 1'b0; // don't care
			MemWrite 	= 1'b0;
			IRWrite  	= 1'b0;
			
			RegSrc		= 2'b10; 
			
			RegWrite 	= 1'b0;
			ImmSrc   	= 2'b01; // don't care
			ALUSrcA  	= 1'b0;
			ALUSrcB  	= 2'b01;
			ALUControl 	= 4'b0100; // ADD
			ResultSrc 	= 2'b00;	// don't care
			
			Z_enable = 1'b1;
			
			BLenable = 1'b0;
			BXenable = 1'b0;
			
			// REMARK: For both LDR and STR, Rn must be chosen (X0)
			//			  For STR, Rd must be connected to RA2 (10)
			//			  No need for Rm

			end 
			
		// Data Processing Instruction
		2'b00: // Execute ALU Cycle (Cycle 3)
			begin
			
			PCWrite 		= 1'b0; // don't care
			AdrSrc   	= 1'b0; // don't care
			MemWrite 	= 1'b0; // don't care
			IRWrite  	= 1'b0; // don't care
			
			RegSrc		= 2'b00; 
				  
			RegWrite 	= 1'b0;			// not yet
			ImmSrc   	= 2'b00; 		// don't care
			ALUSrcA  	= 1'b0;			// Choose Rn
			ALUSrcB  	= 2'b00;			// Choose Rm
			ALUControl 	= {Funct[4:1]};// Choose Operation
			ResultSrc 	= 2'b00;			// don't care
			
			Z_enable = 1'b1;
			
			BLenable = 1'b0;
			BXenable = 1'b0;
			
			end 
			
		2'b10: // Branch Cycle (Cycle 3)
			begin
			
			PCWrite 		= CondEx ? 1'b1 : 1'b0 ; // !
			AdrSrc   	= 1'b0; // don't care
			MemWrite 	= 1'b0; // don't care
			IRWrite  	= 1'b0; // don't care
				  
			RegSrc		= 2'b01; // X1
			
			RegWrite 	= 1'b0;
			ImmSrc   	= 2'b10;   // Op
			ALUSrcA  	= 1'b0; 	  // Choose Rn
			ALUSrcB  	= 2'b01;   // Choose ExtImm
			ALUControl 	= 4'b1101; // MOVE 
			ResultSrc 	= 2'b10;	  // don't wait another cycle
			
			Z_enable = 1'b1;
			
			if({Funct[5:4]} == 2'b10) 
				BLenable = 1'b1;
			else
				BLenable = 1'b0;
			if({Funct[5:4]} == 2'b11) 
				BXenable = 1'b1;
			else
				BXenable = 1'b0;
			
			end 
			
		default: begin
		
			PCWrite 		= 1'b0; 
			AdrSrc   	= 1'b0; 
			MemWrite 	= 1'b0;
			IRWrite  	= 1'b0; 
			
			RegSrc 		= 2'b00;
				  
			RegWrite 	= 1'b0; 
			ImmSrc   	= 2'b00; 
			ALUSrcA  	= 1'b0;
			ALUSrcB  	= 2'b00;
			ALUControl 	= 4'b0000; 
			ResultSrc 	= 2'b00;	
			
			Z_enable = 1'b1;
			
			BLenable = 1'b0;
			BXenable = 1'b0;
		
		
		end
			
			
		endcase

end

else if(state == 3) begin 

	case(Op)
		
		2'b01: 
			begin
			
			// MemRead/MemWrite Cycle (Cycle 4)
				

			PCWrite 		= 1'b0; 
			AdrSrc   	= 1'b1; 
			MemWrite 	= ~Funct[0]; 
			IRWrite  	= 1'b0; 
				  
			RegSrc 		= 2'b00;
			
			RegWrite 	= 1'b0; // RegWrite is at Writeback
			ImmSrc   	= 2'b01; 
			ALUSrcA  	= 1'b0;
			ALUSrcB  	= 2'b01;
			ALUControl 	= 4'b0100; // ADD
			ResultSrc 	= 2'b00;	
			
			Z_enable = 1'b1;
			
			BLenable = 1'b0;
			BXenable = 1'b0;
			
			// REMARK: 	Funct[0] = 0 (STR), Funct[0] = 1 (LDR)
			//				MemWritre = 1		, MemWritre = 0
			end 
			
		2'b00: 
			begin
			
			// ALUWB Cycle (Cycle 4)
			
			PCWrite 		= 1'b0; // don't care
			AdrSrc   	= 1'b0; // don't care
			MemWrite 	= 1'b0; // don't care
			IRWrite  	= 1'b0; // don't care
			
			RegSrc 		= 2'b00; // don't care (not decoded yet)
				  
			
			ImmSrc   	= 2'b00; 		// don't care
			ALUSrcA  	= 1'b0;			// don't care
			ALUSrcB  	= 2'b00;			// don't care
			
			
			case(Funct[4:1])
			
				4'b1010: // FOR CMP, DO SUB BUT DO NOT WRITE TO REGISTER
					begin
					ALUControl = 4'b0010;
					RegWrite 	= 1'b0;	
					end
				
				default: 
					begin
					ALUControl = {Funct[4:1]};
					RegWrite 	= 1'b1;	
					end
			endcase
			
			ResultSrc 	= 2'b00;			// !
			
			Z_enable = 1'b1;
			
			BLenable = 1'b0;
			BXenable = 1'b0;
			
			
			end 
			
		2'b10: // Hold the previous Branch Cycle (Cycle 3)
			begin
			
			PCWrite 		= CondEx ? 1'b1 : 1'b0 ; // !
			AdrSrc   	= 1'b0; // don't care
			MemWrite 	= 1'b0; // don't care
			IRWrite  	= 1'b0; // don't care
				  
			RegSrc		= 2'b01; // X1
			
			RegWrite 	= 1'b0;
			ImmSrc   	= 2'b10;   // Op
			ALUSrcA  	= 1'b0; 	  // Choose Rn
			ALUSrcB  	= 2'b01;   // Choose ExtImm
			ALUControl 	= 4'b1101; // ADD  
			ResultSrc 	= 2'b10;	  // don't wait another cycle
			
			Z_enable = 1'b1;
			
			if({Funct[5:4]} == 2'b10) 
				BLenable = 1'b1;
			else
				BLenable = 1'b0;
			if({Funct[5:4]} == 2'b11) 
				BXenable = 1'b1;
			else
				BXenable = 1'b0;
			
			
			end 
			
		default: begin
		
			PCWrite 		= 1'b0; 
			AdrSrc   	= 1'b0; 
			MemWrite 	= 1'b0;
			IRWrite  	= 1'b0; 
			
			RegSrc 		= 2'b00;
				  
			RegWrite 	= 1'b0; 
			ImmSrc   	= 2'b00; 
			ALUSrcA  	= 1'b0;
			ALUSrcB  	= 2'b00;
			ALUControl 	= 4'b0000; 
			ResultSrc 	= 2'b00;
			
			Z_enable = 1'b1;
			
			BLenable = 1'b0;
			BXenable = 1'b0;
		
		
		
		end
			
		endcase

end

else if(state == 4) begin 

	// If LDR
	if((Op == 2'b01) && (Funct[0] == 1)) begin
	
		// Writeback (Cycle 5)

		PCWrite 		= 1'b0; 
		AdrSrc   	= 1'b1; 
		MemWrite 	= 1'b0;
		IRWrite  	= 1'b0; 
		
		RegSrc 		= 2'b00;
			  
		RegWrite 	= 1'b1; // !
		ImmSrc   	= 2'b01; 
		ALUSrcA  	= 1'b0;
		ALUSrcB  	= 2'b01;
		ALUControl 	= 4'b0100; // ADD
		ResultSrc 	= 2'b01;	// Data to WD3
		
		Z_enable = 1'b0;
		
		BLenable = 1'b0;
		BXenable = 1'b0;
		
	end
	
	else begin
	
		PCWrite 		= 1'b0; 
		AdrSrc   	= 1'b0; 
		MemWrite 	= 1'b0;
		IRWrite  	= 1'b0; 
		
		RegSrc 		= 2'b00;
			  
		RegWrite 	= 1'b0; 
		ImmSrc   	= 2'b00; 
		ALUSrcA  	= 1'b0;
		ALUSrcB  	= 2'b00;
		ALUControl 	= 4'b0000; 
		ResultSrc 	= 2'b00;	
		
		Z_enable = 1'b0;
		
		BLenable = 1'b0;
		BXenable = 1'b0;
	
	end

end



end


endmodule

