module Extender(
input [23:0] A,
input [1:0] select,
output reg [31:0] Q

);

reg [31: 0] res;

always@(*) begin

if(select == 2'b00)
	Q = {24'b0, A[7:0]};

else if(select == 2'b01)
	Q = {20'b0, A[11:0]};
	
else if(select == 2'b10)
	Q = {{6{A[23]}}, A[23:0], 2'b00};
	
else
	Q = {24'b0, A[7:0]};


end

 
endmodule
