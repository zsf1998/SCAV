module full_adder ( a , b , carry_in , sum , carry_out );
input wire a,b,carry_in;
output wire sum,carry_out;
wire c1,c2,s1;
wire [6:0] count;
wire [6:0] v;

half_adder ha1
(
.a (a) ,
.b (b) ,
.sum (s1) ,
.carry (c1) 
);
half_adder ha2
(
.a (s1) ,
.b (carry_in) ,
.sum (sum) ,
.carry (c2) 
);
assign carry_out=c1|c2 ;

endmodule
