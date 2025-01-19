module SM3_Controller ( clk , rst , W , R , finish , count_out , ctrl );
input wire clk;
input wire rst,W,R;
output wire finish;
output wire [6:0] count_out;
output wire [1:0] ctrl;
wire [6:0] count;
wire [1:0] next_state,current_state;
wire [6:0] count_plus;
reg  neg_out,neg_cnt;
wire pwm_rising_edge;
wire [31:0] FF,FF_0,FF_1;
wire [31:0] W0,Wj_0,W1,W2,W3,W4;

assign count_plus=W0^W1^{W2[16:0],W3[31:17]} ;
assign ctrl=W1^{W2[16:0],W2[31:17]}^W3 ;
assign ctr=(W0&W1)|(W0&W2)|(W1&W2) ;

always @( posedge clk or  posedge rst)
begin
  if(neg_out||neg_cnt&&rst&&clk)
    begin
    neg_out<=pwm_rising_edge?neg_cnt:neg_out;
    end
  else if(neg_out||neg_cnt&&rst&&clk)
      begin
      neg_out<=neg_cnt;
      end

end
endmodule
