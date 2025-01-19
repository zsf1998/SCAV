module code_83 ( din , dout );
input wire [7:0] din;
output wire [2:0] dout;
wire [2:0] d_out;

assign d_out=func_code(din);
assign dout=d_out;

function [2:0]func_code;
	input [7:0]func_din;
		case(func_din)
			'd128:
			begin
			func_code=7;
			end
			'd64:
			begin
			func_code=6;
			end
			'd32:
			begin
			func_code=5;
			end
			'd16:
			begin
			func_code=4;
			end
			'd8:
			begin
			func_code=3;
			end
			'd4:
			begin
			func_code=2;
			end
			'd2:
			begin
			func_code=1;
			end
			'd0:
			begin
			func_code=0;
			end
			default:
			begin
			func_code=0;
			end

		endcase
endfunction
	
endmodule
