// Control for the FSM

`timescale 1ns/10ps
module SM3_Controller (clk , rst , W , R , finish , count_out , ctrl);

 
input clk , rst , W , R ;

output finish ;
output [6:0] count_out ;    // calculat the times of extend&compress&writeresult 
output [1:0] ctrl ;  

reg  finish ;
reg  [6:0] count_out , count ;
reg  [1:0] next_state , current_state;
wire [6:0] count_plus ;

parameter idle = 'b00;                //idle state, no operation
parameter write = 'b01;	            // write register 
parameter encryption = 'b10;	    // encryption only
parameter read = 'b11;		    	// read register
	
assign count_plus = count + 'd1 ;  //the current state is assigned to output wire
assign ctrl = next_state ;       // counter ,to control the process of the sm3 algorithm
 
always@(posedge clk or negedge rst)  //current_state reg
     begin
        if(!rst)
           begin
              current_state <= idle ;
           end
        else
           begin
              current_state <= next_state;
           end
     end
always@(posedge clk or negedge rst) //next_state logic
     begin
        if(!rst)
			begin 
              next_state <= idle ;
			end
        else
			begin
             case(current_state)
                 idle:
                    begin
                      if(W == 'b1)		
						begin
                         next_state <= write ;     
						end
					  else if(R == 'b1)
							begin
							 next_state <= read ;
							end
                      else
						begin
                         next_state <= idle ;
						end
                    end
                  write:
                    begin
                      if(count < 'd16)
						begin
                          next_state <= write ;
						end
                      else
						begin
                          next_state <= encryption ;
						end
                   end
                 encryption:
                    begin
                      if(count < 'd69)
						begin
                             next_state <= encryption ;
						end
                      else
						begin
                             if(R == 'b1)
								begin
                                 next_state <= read ;
								end
                             else
								begin
                                 next_state <= idle ;
								end
						end
                    end
                read:
                    begin
                        next_state <= idle ;
                    end
//              default
//                    next_state <= idle ;
             endcase
			end
       end
            
//output logic
// at each state , we can output signals
always @(posedge clk or negedge rst)
    begin
       if(!rst)
         begin 
           count <= 'd0;
           finish <= 'b0 ;
           count_out <= 'd0;
         end
       else
         begin
		   case(next_state)   
           idle:
			begin
				count_out <= 'd0;
                finish <= 'b0 ;
                count <= 'd0;
			end
		   write:
	        begin
                   
				finish <= 'b0 ;
                count <= count_plus ;
				count_out <= count_plus;
            end	
           encryption:
            begin
                    if(count_out< 'd69)
                      begin
                        finish <= 'b0 ;
                        count <= count_plus ;
						count_out <= count_plus;
                      end                      
					else
                       begin
                         finish <= 'b1 ;
                         count <= count_plus ;
                         count_out <=  'd0 ;
                        end
			end
           read:
                 begin
                     finish <= 'b0;
                     count_out <= 'd0;
                     count <= 'd0;
                  end
/*	   default:
		begin
                  finish <= 'b0;
		          count_out <= 'd0;
                  count <= 'd0;
		end*/
		   endcase	
		 end	
    end				
endmodule						          
              
                     

          
      
