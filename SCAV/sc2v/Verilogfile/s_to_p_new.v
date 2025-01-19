module s_to_p ( clk , rst_n , data_a , valid_a , data_b , valid_b , ready_a );
input wire clk;
input wire rst_n;
input wire data_a,valid_a;
output reg [5:0] data_b;
output reg valid_b;
output wire ready_a;
reg [5:0] data_b1;
reg [3:0] cnt;

assign ready_a=1 ;

always @( posedge clk or  negedge rst_n)
begin
  if(!rst_n)
    begin
    data_b<=0;
    data_b1<=0;
    end
  else if(cnt==5&&valid_a==1)
      begin
      data_b<=data_b1;
      end
    else if(valid_a==1)
        begin
        data_b1<={data_a,data_b1[5:1]};
        end
end

always @( posedge clk or  negedge rst_n)
begin
  if(!rst_n)
    begin
    cnt<=0;
    end
  else if(cnt==5)
      begin
      cnt<=0;
      end
    else if(valid_a==1)
        begin
        cnt<=cnt+1;
        end
end

always @( posedge clk or  negedge rst_n)
begin
  if(!rst_n)
    begin
    valid_b<=0;
    end
  else if(cnt==5)
      begin
      valid_b<=1;
      end
    else
      begin
      valid_b<=0;
      end

end
endmodule
