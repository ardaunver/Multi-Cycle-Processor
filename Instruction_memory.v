module Instruction_memory#(parameter BYTE_SIZE=4, parameter ADDR_WIDTH=32)(
input [ADDR_WIDTH-1:0] ADDR,
output [(BYTE_SIZE*8)-1:0] RD 
);

reg [7:0] mem [4095:0];

initial begin

//mem[64]<=8'h0D;
//mem[65]<=8'h0C;
//mem[66]<=8'h0B;
//mem[67]<=8'h0A;
$readmemh("inst_mem.txt", mem); // You will need this for real tests
end
genvar i;
generate
	for (i = 0; i < BYTE_SIZE; i = i + 1) begin: read_generate
		assign RD[8*i+:8] = mem[ADDR+i];
	end
endgenerate
endmodule