`timescale 1ns/10ps
// The initial value 
`define IV_0 32'h7380166f
`define IV_1 32'h4914b2b9
`define IV_2 32'h172442d7
`define IV_3 32'hda8a0600
`define IV_4 32'ha96f30bc
`define IV_5 32'h163138aa
`define IV_6 32'he38dee4d
`define IV_7 32'hb0fb0e4e

// The value for parameter Tj 
`define T0 32'h79cc4519    //  0  <= j <= 15
`define T1 32'h9d8a7a87    //  16 <= j <= 63
module  CompressExtend ( clk , rst , ctrl  ,finish , m_i , Round , wout );

input clk , rst ;
input finish ;
input  [1:0] ctrl ;
input [31:0] m_i ;
input [6:0] Round ;
output [255:0] wout ;
 
reg [255:0] WOUT_0 , wout ;
reg [31:0] W0,W1,W2,W3,W4,W5,W6,W7,W8,W9,W10,W11,W12,W13,W14,W15,Wout67,Wout63,Tj;
reg [31:0] A,B,C,D,E,F,G,H;

wire [31:0] Wj_0_out , W16  , Wj_0 ;
wire [31:0] SS1_0,SS1,SS2,TT1,TT2,FF,GG,next_Tj,next_C,next_E,next_G;
wire [31:0] TT1_0,TT1_1,TT2_0,TT2_1,FF_0,FF_1,GG_0,GG_1;

assign Wj_0 = W0 ^ W7 ^ { W13[16:0],W13[31:17] };
assign W16  =  Wj_0 ^ { Wj_0[16:0],Wj_0[31:17] } ^ { Wj_0[8:0],Wj_0[31:9] } ^ { W3[24:0],W3[31:25] } ^ W10;

assign SS1_0 = {A[19:0],A[31:20]} + E + Tj;
assign SS1 = {SS1_0[24:0],SS1_0[31:25]};
assign SS2 = SS1 ^ {A[19:0],A[31:20]};

assign FF_0 = A^B^C;                     //  0 <= j <= 15   FFj(X,Y,Z) function
assign FF_1 = (A&B)|(A&C)|(B&C);         // 16 <= j <= 63   FFj(X,Y,Z) function
 
assign GG_0 = E^F^G;                     //  0 <= j <= 15   GGj(X,Y,Z) function
assign GG_1 = (E&F)|(~E&G);              // 16 <= j <= 63   GGj(X,Y,Z) function  

assign FF = (Round < 'd21) ? FF_0 : FF_1 ;
assign GG = (Round < 'd21) ? GG_0 : GG_1 ;

assign TT1 = FF + D + SS2 + Wout63; 
assign TT2 = GG + H + SS1 + Wout67;

assign next_Tj = {Tj[30:0],Tj[31]};
assign next_C = {B[22:0],B[31:23]};
assign next_E = TT2^{TT2[22:0],TT2[31:23]}^{TT2[14:0],TT2[31:15]}; 
assign next_G = {F[12:0],F[31:13]};

 always@(posedge clk or negedge rst)
   begin    
    if(!rst)
      begin
        Wout67 <= 'b0 ;
        Wout63 <= 'b0 ;
        wout<='b0; //mod_by_xhhu
       
        A <= `IV_0;
        B <= `IV_1;
        C <= `IV_2;
        D <= `IV_3;
        E <= `IV_4;
        F <= `IV_5;
        G <= `IV_6;
        H <= `IV_7; 
        Tj <= `T0 ;
        WOUT_0[255:224] <= `IV_0;
        WOUT_0[223:192] <= `IV_1;
        WOUT_0[191:160] <= `IV_2;
        WOUT_0[159:128] <= `IV_3;
        WOUT_0[127:96]  <= `IV_4;
        WOUT_0[95:64]   <= `IV_5;
        WOUT_0[63:32]   <= `IV_6;
        WOUT_0[31:0]    <= `IV_7; 



        //mod_by_xhhu 
        W0 <= 32'b0;
        W1 <= 32'b0;
        W2 <= 32'b0;
        W3 <= 32'b0;
        W4 <= 32'b0;
        W5 <= 32'b0;
        W6 <= 32'b0;
        W7 <= 32'b0;
        W8 <= 32'b0;
        W9 <= 32'b0;
        W10 <= 32'b0;
        W11 <= 32'b0;
        W12 <= 32'b0;
        W13 <= 32'b0;
        W14 <= 32'b0;
        W15 <= 32'b0;
        // mod end
      end
    else
      begin   
        if( ctrl == 'b01 || ctrl == 'b10)    // message extend + compress
          begin  
            case ( Round )
                   'd0 : 
                      begin  
                        W0 <= m_i ; 
                        
                      end
                   'd1 : 
                      begin  
                        W1 <= m_i ;
                        
                      end
                   'd2 : 
                      begin  
                        W2 <= m_i ; 
                        
                      end
                   'd3 : 
                      begin  
                        W3 <= m_i ; 
                       
                      end
                   'd4 :            
                      begin  
                        W4 <= m_i ; 
                        Wout67 <= W0 ;        // used in TT1 function 
                        Wout63 <= W0 ^ m_i ;  // start calculation 
                        Tj <= `T0 ;
                      end
                   'd5 :                    
                      begin  
                        W5 <= m_i ;
 
                        Wout67 <= W1 ; // used in TT1 function 
                        Wout63 <= W1 ^ m_i ; // start calculation j=0  

                        Tj <= next_Tj; // used the last value in SS1 function

                        A <= TT1;     // message compress
			B <= A;
			C <= next_C;
		        D <= C;
			E <= next_E;
			F <= E;
			G <= next_G;
			H <= G;
                       
                      end
                   'd6 :    //j = 1
                      begin  
                        W6 <= m_i ; 

                        Wout67 <= W2 ; 
                        Wout63 <= W2 ^ m_i ; 

                        Tj <= next_Tj;
                        
                        A <= TT1;
			B <= A;
			C <= next_C;
		        D <= C;
			E <= next_E;
			F <= E;
			G <= next_G;
			H <= G;
                       
                      end
                   'd7 :   //2
                      begin  
                        W7 <= m_i ; 
                        Wout67 <= W3 ; 
                        Wout63 <= W3 ^ m_i ; 

                        Tj <= next_Tj;
                       
                        A <= TT1;
			B <= A;
			C <= next_C;
		        D <= C;
			E <= next_E;
			F <= E;
			G <= next_G;
			H <= G;
                
                      end
                   'd8 : 
                      begin  
                        W8 <= m_i ; 
                        Wout67 <= W4 ;
                        Wout63 <= W4 ^ m_i ; 

                        Tj <= next_Tj;
                                            
                        A <= TT1;
			B <= A;
			C <= next_C;
		        D <= C;
			E <= next_E;
			F <= E;
			G <= next_G;
			H <= G;
                                 
                      end
                   'd9 : 
                      begin 
                        W9 <= m_i ; 
                        Wout67 <= W5 ;
                        Wout63 <= W5 ^ m_i ;

                        Tj <= next_Tj;
                        
                        A <= TT1;
			B <= A;
			C <= next_C;
		        D <= C;
			E <= next_E;
			F <= E;
			G <= next_G;
			H <= G; 
                
                      end
                   'd10 : 
                      begin  
                        W10 <= m_i ; 
                        Wout67 <= W6 ;
                        Wout63 <= W6 ^ m_i ; 

                        Tj <= next_Tj;
                        
                        A <= TT1;
			B <= A;
			C <= next_C;
		        D <= C;
			E <= next_E;
			F <= E;
			G <= next_G;
			H <= G;
                       
                      end
                   'd11 : 
                      begin  
                        W11 <= m_i ; 
                        Wout67 <= W7 ;
                        Wout63 <= W7 ^ m_i ;
 
                        Tj <= next_Tj;
                     
                        A <= TT1;
			B <= A;
			C <= next_C;
		        D <= C;
			E <= next_E;
			F <= E;
			G <= next_G;
			H <= G;
                      
                      end
                   'd12 : 
                      begin  
                        W12 <= m_i ; 
                        Wout67 <= W8 ;
                        Wout63 <= W8 ^ m_i ;
 
                        Tj <= next_Tj;
                        
                        A <= TT1;
			B <= A;
			C <= next_C;
		        D <= C;
			E <= next_E;
			F <= E;
			G <= next_G;
			H <= G;
                      
                      end
                   'd13 : 
                      begin  
                        W13 <= m_i ; 
                        Wout67 <= W9 ;
                        Wout63 <= W9 ^ m_i ; 

                        Tj <= next_Tj;
                        
                        A <= TT1;
			B <= A;
			C <= next_C;
		        D <= C;
			E <= next_E;
			F <= E;
			G <= next_G;
			H <= G;
                      
                      end
                   'd14 : 
                      begin  
                        W14 <= m_i ; 
                        Wout67 <= W10 ;
                        Wout63 <= W10 ^ m_i ; 

                        Tj <= next_Tj;
                        
                        A <= TT1;
			B <= A;
			C <= next_C;
		        D <= C;
			E <= next_E;
			F <= E;
			G <= next_G;
			H <= G;
                     
                         
                      end
                   'd15 : 
                      begin  
                        W15 <= m_i ; 
                        Wout67 <= W11 ;
                        Wout63 <= W11 ^ m_i; 

                        Tj <= next_Tj;
                        
                        A <= TT1;
			B <= A;
			C <= next_C;
		        D <= C;
			E <= next_E;
			F <= E;
			G <= next_G;
			H <= G;
                      
                          
                      end   
                   'd16,
                   'd17, 
                   'd18, 
                   'd19 :   // j=14
                      begin  
                            Wout67 <= W12 ;
                            Wout63 <= W12 ^ W16 ;

                            Tj <= next_Tj;
                           
                            A <= TT1;
			    B <= A;
			    C <= next_C;
		            D <= C;
			    E <= next_E;
			    F <= E;
			    G <= next_G;
			    H <= G;
                            W0  <= W1;
		            W1  <= W2;
		            W2  <= W3;
	                    W3  <= W4;
		            W4  <= W5;
		            W5  <= W6;
		            W6  <= W7;
		            W7  <= W8;
		            W8  <= W9;
	                    W9  <= W10;
		            W10 <= W11;
	                    W11 <= W12;
		            W12 <= W13;
		            W13 <= W14;
		            W14 <= W15;
		            W15 <= W16;
                 
                          
                    
                      end  
                   'd20 :   // j=15
                      begin  
                            Wout67 <= W12 ;
                            Wout63 <= W12 ^ W16 ;

                            Tj <= `T1;    // prepare for j=16
                          
                            A <= TT1;
			    B <= A;
			    C <= next_C;
		            D <= C;
			    E <= next_E;
			    F <= E;
			    G <= next_G;
			    H <= G;
                            W0  <= W1;
		            W1  <= W2;
		            W2  <= W3;
	                    W3  <= W4;
		            W4  <= W5;
		            W5  <= W6;
		            W6  <= W7;
		            W7  <= W8;
		            W8  <= W9;
	                    W9  <= W10;
		            W10 <= W11;
	                    W11 <= W12;
		            W12 <= W13;
		            W13 <= W14;
		            W14 <= W15;
		            W15 <= W16;
                      
                      end  

                   'd21,   //j = 16  Tj
                   'd22, 
                   'd23,
                   'd24, 
                   'd25,
                   'd26, 
                   'd27,
                   'd28,
                   'd29,
                   'd30, 
                   'd31,
                   'd32, 
                   'd33,
                   'd34, 
                   'd35,
                   'd36, 
                   'd37,
                   'd38, 
                   'd39,
                   'd40,
                   'd41,
                   'd42, 
                   'd43,
                   'd44, 
                   'd45,
                   'd46, 
                   'd47,
                   'd48, 
                   'd49,
                   'd50, 
                   'd51,
                   'd52,
                   'd53,
                   'd54, 
                   'd55,
                   'd56, 
                   'd57,
                   'd58, 
                   'd59,
                   'd60, 
                   'd61,
                   'd62, 
                   'd63,
                   'd64,
                   'd65,
                   'd66, 
                   'd67 :
                       begin  
                            Wout67 <= W12 ;
                            Wout63 <= W12 ^ W16 ;

                            Tj <= next_Tj;
                            
                            A <= TT1;
			    B <= A;
			    C <= next_C;
		            D <= C;
			    E <= next_E;
			    F <= E;
			    G <= next_G;
			    H <= G;
                            W0  <= W1;
		            W1  <= W2;
		            W2  <= W3;
	                    W3  <= W4;
		            W4  <= W5;
		            W5  <= W6;
		            W6  <= W7;
		            W7  <= W8;
		            W8  <= W9;
	                    W9  <= W10;
		            W10 <= W11;
	                    W11 <= W12;
		            W12 <= W13;
		            W13 <= W14;
		            W14 <= W15;
		            W15 <= W16;
                end
                   'd68 : 
                      begin  
                            Wout67 <= W12 ;
                            Wout63 <= W12 ^ W16 ;

                            Tj <= next_Tj;
                            
                            A <= TT1;
			    B <= A;
			    C <= next_C;
		            D <= C;
			    E <= next_E;
			    F <= E;
			    G <= next_G;
			    H <= G;
                            W0  <= W1;
		            W1  <= W2;
		            W2  <= W3;
	                    W3  <= W4;
		            W4  <= W5;
		            W5  <= W6;
		            W6  <= W7;
		            W7  <= W8;
		            W8  <= W9;
	                    W9  <= W10;
		            W10 <= W11;
	                    W11 <= W12;
		            W12 <= W13;
		            W13 <= W14;
		            W14 <= W15;
		            W15 <= W16;
            
			 WOUT_0[255:224] <= TT1 ^ WOUT_0[255:224];
			 WOUT_0[223:192] <= A ^ WOUT_0[223:192];
			 WOUT_0[191:160] <= next_C ^ WOUT_0[191:160];
			 WOUT_0[159:128] <= C ^ WOUT_0[159:128];
			 WOUT_0[127:96]  <= next_E ^  WOUT_0[127:96];
			 WOUT_0[95:64]   <= E ^ WOUT_0[95:64];
			 WOUT_0[63:32]   <= next_G ^  WOUT_0[63:32];
			 WOUT_0[31:0]    <= G ^ WOUT_0[31:0];
			end
                   'd69:	
                        begin
		                 A <= WOUT_0[255:224];
                         B <= WOUT_0[223:192];
                         C <= WOUT_0[191:160];
                         D <= WOUT_0[159:128];
                         E <= WOUT_0[127:96];
                         F <= WOUT_0[95:64];
                         G <= WOUT_0[63:32] ;
                         H <= WOUT_0[31:0];
                         wout[255:224] <= WOUT_0[255:224];
                         wout[223:192]<= WOUT_0[223:192];
                         wout[191:160] <= WOUT_0[191:160];
                         wout[159:128] <= WOUT_0[159:128];
                         wout[127:96] <= WOUT_0[127:96];
                         wout[95:64] <= WOUT_0[95:64];
                         wout[63:32] <= WOUT_0[63:32] ;
                         wout[31:0] <= WOUT_0[31:0];
                        end
                   default: ;
                             
               endcase
           end
           //end
        else 
                 begin
                    if ( ctrl == 'b11 )
                        begin
                             Wout67 <= 'b0 ;
                             Wout63 <= 'b0 ;
       
                             A <= `IV_0;
                             B <= `IV_1;
                             C <= `IV_2;
                             D <= `IV_3;
                             E <= `IV_4;
                             F <= `IV_5;
                             G <= `IV_6;
                             H <= `IV_7; 
                             Tj <= `T0 ;
                             WOUT_0[255:224] <= `IV_0;
                             WOUT_0[223:192] <= `IV_1;
                             WOUT_0[191:160] <= `IV_2;
                             WOUT_0[159:128] <= `IV_3;
                             WOUT_0[127:96]  <= `IV_4;
                             WOUT_0[95:64]   <= `IV_5;
                             WOUT_0[63:32]   <= `IV_6;
                             WOUT_0[31:0]    <= `IV_7; 
                          end 
                 end
         
        end 
   end

endmodule



