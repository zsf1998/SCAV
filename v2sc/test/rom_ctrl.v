
`timescale  1ns/1ns
module  rom_ctrl
#(
    parameter   CNT_MAX = 24'd9_999_999
)
(
    input   wire            sys_clk     ,
    input   wire            sys_rst_n   ,
    input   wire            key1        ,
    input   wire            key2        ,

    output  reg     [7:0]   addr

);

reg     [23:0]  cnt_200ms   ;
reg             key1_en     ;
reg             key2_en     ;

always@(posedge sys_clk or negedge sys_rst_n)
  begin
    if(sys_rst_n == 1'b0)
		begin
			cnt_200ms <=  24'b0;
		end
    else    if(cnt_200ms == CNT_MAX || key1_en == 1'b1 || key2_en == 1'b1)
		begin
			cnt_200ms   <=  24'd0;
		end
    else
		begin
        cnt_200ms   <=  cnt_200ms + 1'b1;
		end
  end

always@(posedge sys_clk or negedge sys_rst_n)
  begin
    if(sys_rst_n == 1'b0)
		begin
			key1_en <=  1'b0;
		end
    else    if(key2 == 1'b1)
		begin
			key1_en <=  1'b0;
		end
    else    if(key1 == 1'b1)
		begin
			key1_en <= ~key1_en;
		end
    else
		begin
			key1_en <= key1_en;
		end
  end

always@(posedge sys_clk or negedge sys_rst_n)
  begin
    if(sys_rst_n    == 1'b0)
		begin
			key2_en <=  1'b0;
		end
    else    if(key1 == 1'b1)
		begin
			key2_en <=  1'b0;
		end
    else    if(key2 == 1'b1)
		begin
			key2_en <= ~key2_en;
		end
    else
		begin
			key2_en <= key2_en;
		end
  end

always@(posedge sys_clk or negedge sys_rst_n)
  begin
    if(sys_rst_n == 1'b0)
		begin
			addr    <=  8'd0;
		end
    else    if(addr == 8'd255 && cnt_200ms == CNT_MAX)
		begin
			addr    <=  8'd0;
		end
    else    if(key1_en == 1'b1)
		begin
			addr    <=  8'd99;
		end
    else    if(key2_en == 1'b1)
		begin
			addr    <=  8'd199;
		end
    else    if(cnt_200ms == CNT_MAX)
		begin
			addr    <=  addr + 1'b1;
		end
  end		
		
endmodule

