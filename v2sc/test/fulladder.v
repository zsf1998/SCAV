//fulladder
module fulladder(
                  input a,             //加数1
                  input b,             //加数2
                  input carry_in,      //低位向高位的进位
                  output sum,          //两个数的加和
                  output carry_out     //加数和的进位
                  );

wire s1;
wire c1;
wire c2;
halfadder ha1(
           .a(a),
           .b(b),
           .sum(s1),
           .carry(c1)
             );

halfadder ha2(
           .a(s1),
           .b(carry_in),
           .sum(sum),
           .carry(c2)
             );
assign carry_out=c1|c2;
endmodule