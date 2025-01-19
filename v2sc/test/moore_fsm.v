module moore_fsm(in,clk,rst,out);
input in;
input clk;
input rst;
output reg out;
reg [2:0]current_state;
reg [2:0] next_state;

parameter S0='d0;
parameter S1='d1;
parameter S2='d2;
parameter S3='d3;
parameter S4='d4;


//状态转移
always@(posedge clk or negedge rst)
begin
	if (!rst)
		begin
		current_state<=S0;
		end
	else 
		begin
		current_state<=next_state;
		end
end

//状态转移条件
always@(*)
	begin
		case(current_state)
			S0:
				begin
				next_state=in?S1:S0;
				end
			S1:
				begin
				next_state=in?S1:S2;
				end
			S2:
				begin
				next_state=in?S3:S0;
				end
			S3:
				begin
				next_state=in?S4:S2;
				end
			S4:
				begin
				next_state=in?S1:S0;		
				end
			default: 
				begin
				next_state=S0;
				end
		endcase
	end
	
//输出
always@ (posedge clk or negedge rst)
begin
	if (!rst)
		begin
		out=0;
		end
	else
		begin
		case(next_state)  //判断next_state会在接收到最后一个信号的同时输出脉冲
			S0:
				begin
				out<=0;
				end
			S1:
				begin
				out<=0;
				end
			S2:
				begin
				out<=0;
				end
			S3:
				begin
				out<=0;
				end
			S4:
				begin
				out<=1;
				end
			default:;
		endcase
		end
end	
	
endmodule