module half_adder ( a , b , sum , carry );
input wire a,b;
output wire sum,carry;

assign sum=a^b ;
assign carry=a&b ;

endmodule
