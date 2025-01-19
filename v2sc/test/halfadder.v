	// halfadder
	module halfadder(
		output       sum,  //sum
		output       carry_out, //carry
		input        a,  
		input        b
					 );

	assign    sum  = a ^ b;
	assign    carry_out = a & b;

	endmodule




