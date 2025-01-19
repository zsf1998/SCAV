module code_83 ( din , dout );
input wire [7:0] din;
output wire [2:0] dout;
wire [2:0] out;

assign out=func_code(din) ;
assign dout=out ;

function [2,0] func_code
begin
input [7:0]func_din
    case(func_din)
        128:
        begin
        func_code=7;
        end

        64:
        begin
        func_code=6;
        end

        32:
        begin
        func_code=5;
        end

        16:
        begin
        func_code=4;
        end

        8:
        begin
        func_code=3;
        end

        4:
        begin
        func_code=2;
        end

        2:
        begin
        func_code=1;
        end

        0:
        begin
        func_code=0;
        end

        default:
        begin
        func_code=0;
        end

        endcase


end
endfunction
endmodule
