module moore_fsm ( in , clk , rst , out );
input reg in;
input wire clk;
input wire rst;
output reg out;
reg [2:0] current_state;
reg [2:0] next_state;


always @( * )
begin
    case(current_state)
        0:
        begin
        next_state=in?1:0;
        end

        1:
        begin
        next_state=in?1:2;
        end

        2:
        begin
        next_state=in?3:0;
        end

        3:
        begin
        next_state=in?4:2;
        end

        4:
        begin
        next_state=in?1:0;
        end

        default:
        begin
        end

        endcase

end

always @( posedge clk or  negedge rst)
begin
  if(!rst)
    begin
    current_state<=0;
    end
  else
    begin
    current_state<=next_state;
    end
end

always @( posedge clk or  negedge rst)
begin
  if(!rst)
    begin
    out<=0;
    end
  else
    begin
        case(next_state)
            0:
            begin
            out<=0;
            end

            1:
            begin
            out<=0;
            end

            2:
            begin
            out<=0;
            end

            3:
            begin
            out<=0;
            end

            4:
            begin
            out<=1;
            end

            default:
            begin
            end

            endcase

    end

end
endmodule
