module even_divide3(clk,rst,clk3);
input clk;
input rst;
output clk3;

reg [1:0] cnt;
reg clk1;
reg clk2;

always@(posedge clk or negedge rst)
begin
    if (!rst)   
		begin
			cnt<=0;
		end
     else if (cnt==2)
		begin 
			cnt<=0;
		end
     else 
		begin
			cnt<=cnt+1;
		end
end

always@(posedge clk or negedge rst)
begin
    if(!rst)
		begin
			clk1<=0;
		end
    else if (cnt==1)
		begin 
			clk1<=0;
		end
    else if (cnt==2)
		begin 
			clk1<=1;
		end

end  

always@(negedge clk or negedge rst)
begin
    if(!rst)
		begin
			clk2<=0;
		end
    else if (cnt==0)
		begin
			clk2<=1;
		end
    else if (cnt==2)
		begin 
			clk2<=0;
		end

end  

assign clk3=clk1&clk2;

endmodule