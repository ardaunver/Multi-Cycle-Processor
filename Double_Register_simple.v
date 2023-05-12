module Double_Register_simple #(
     parameter WIDTH=8)
    (
	  input  clk, reset,
	  input	[WIDTH-1:0] DATA1, DATA2,
	  output reg [WIDTH-1:0] OUT1, OUT2
    );
	 
always@(posedge clk) begin
	if(reset == 1'b0) begin
		OUT1<=DATA1;
		OUT2<=DATA2;
		end
	else begin
		OUT1<={WIDTH{1'b0}};
		OUT2<={WIDTH{1'b0}};
		end
end
	 
endmodule	 