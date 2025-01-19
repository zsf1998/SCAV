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
wire  pwm_rising_edge;
wire pwm_rising_edge1;
wire [31:0] FF,FF_0,FF_1;

assign count_plus=pwm_rising_edge1 ? 1:neg_cnt ;
assign ctrl=pwm_rising_edge ? neg_cnt:neg_out ;
assign ctr=ctrl[1:0] ? neg_cnt:1 ;
assign ct=rst ? clk:(neg_cnt+neg_out)neg_out ;

always @( posedge clk or  posedge rst)
begin
neg_out<=pwm_rising_edge1?neg_cnt:neg_out;
neg_out<=pwm_rising_edge1?1:neg_cnt;
neg_out<=(pwm_rising_edge>1)?neg_cnt:1;
neg_out<=(pwm_rising_edge!=10)?neg_cnt:1;
neg_out<=(pwm_rising_edge<=10)?1:neg_out;

end
endmodule
