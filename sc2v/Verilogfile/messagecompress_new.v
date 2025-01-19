module CompressExtend ( clk , rst , finish , ctrl , m_i , Round , wout );
input wire clk,rst;
input wire finish;
input wire [1:0] ctrl;
input wire [31:0] m_i;
input wire [6:0] Round;
output reg [31:0] wout;
reg [255:0] WOUT_0;
reg [31:0] W0,W1,W2,W3,W4,W5,W6,W7,W8,W9,W10,W11,W12,W13,W14,W15,Wout67,Wout63,Tj;
reg [31:0] A,B,C,D,E,F,G,H;
wire [31:0] Wj_0_out,W16,Wj_0;
wire [31:0] SS1_0,SS1,SS2,TT1,TT2,FF,GG,next_Tj,next_C,next_E,next_G;
wire [31:0] TT1_0,TT1_1,TT2_0,TT2_1,FF_0,FF_1,GG_0,GG_1;

assign Wj_0=W0^W7^{W13[16:0],W13[31:17]} ;
assign W16=Wj_0^{Wj_0[16:0],Wj_0[31:17]}^{Wj_0[8:0],Wj_0[31:9]}^{W3[24:0],W3[31:25]}^W10 ;
assign SS1_0={A[19:0],A[31:20]}+E+Tj ;
assign SS1={SS1_0[24:0],SS1_0[31:25]} ;
assign SS2=SS1^{A[19:0],A[31:20]} ;
assign FF_0=A^B^C ;
assign FF_1=(A&B)|(A&C)|(B&C) ;
assign GG_0=E^F^G ;
assign GG_1=(E&F)|(~E&G) ;
assign FF=(Round<21) ? FF_0:FF_1 ;
assign GG=(Round<21) ? GG_0:GG_1 ;
assign TT1=FF+D+SS2+Wout63 ;
assign TT2=GG+H+SS1+Wout67 ;
assign next_Tj={Tj[30:0],Tj[31]} ;
assign next_C={B[22:0],B[31:23]} ;
assign next_E=TT2^{TT2[22:0],TT2[31:23]}^{TT2[14:0],TT2[31:15]} ;
assign next_G={F[12:0],F[31:13]} ;

always @( posedge clk or  negedge rst)
begin
  if(!rst)
    begin
    Wout67<=0;
    Wout63<=0;
    wout<=0;
    A<=32'h7380166f;
    B<=32'h4914b2b9;
    C<=32'h172442d7;
    D<=32'hda8a0600;
    E<=32'ha96f30bc;
    F<=32'h163138aa;
    G<=32'he38dee4d;
    H<=32'hb0fb0e4e;
    Tj<=32'h79cc4519;
    WOUT_0[255:224]<=32'h7380166f;
    WOUT_0[223:192]<=32'h4914b2b9;
    WOUT_0[191:160]<=32'h172442d7;
    WOUT_0[159:128]<=32'hda8a0600;
    WOUT_0[127:96]<=32'ha96f30bc;
    WOUT_0[95:64]<=32'h163138aa;
    WOUT_0[63:32]<=32'he38dee4d;
    WOUT_0[31:0]<=32'hb0fb0e4e;
    W0<=0;
    W1<=0;
    W2<=0;
    W3<=0;
    W4<=0;
    W5<=0;
    W6<=0;
    W7<=0;
    W8<=0;
    W9<=0;
    W10<=0;
    W11<=0;
    W12<=0;
    W13<=0;
    W14<=0;
    W15<=0;
    end
  else
    begin
      if(ctrl==1||ctrl==2)
        begin
            case(Round)
                0:
                begin
                W0<=m_i;
                end

                1:
                begin
                W1<=m_i;
                end

                2:
                begin
                W2<=m_i;
                end

                3:
                begin
                W3<=m_i;
                end

                4:
                begin
                W4<=m_i;
                Wout67<=W0;
                Wout63<=W0^m_i;
                Tj<=32'h79cc4519;
                end

                5:
                begin
                W5<=m_i;
                Wout67<=W1;
                Wout63<=W1^m_i;
                Tj<=next_Tj;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                end

                6:
                begin
                W6<=m_i;
                Wout67<=W2;
                Wout63<=W2^m_i;
                Tj<=next_Tj;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                end

                7:
                begin
                W7<=m_i;
                Wout67<=W3;
                Wout63<=W3^m_i;
                Tj<=next_Tj;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                end

                8:
                begin
                W8<=m_i;
                Wout67<=W4;
                Wout63<=W4^m_i;
                Tj<=next_Tj;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                end

                9:
                begin
                W9<=m_i;
                Wout67<=W5;
                Wout63<=W5^m_i;
                Tj<=next_Tj;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                end

                10:
                begin
                W10<=m_i;
                Wout67<=W6;
                Wout63<=W6^m_i;
                Tj<=next_Tj;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                end

                11:
                begin
                W11<=m_i;
                Wout67<=W7;
                Wout63<=W7^m_i;
                Tj<=next_Tj;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                end

                12:
                begin
                W12<=m_i;
                Wout67<=W8;
                Wout63<=W8^m_i;
                Tj<=next_Tj;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                end

                13:
                begin
                W13<=m_i;
                Wout67<=W9;
                Wout63<=W9^m_i;
                Tj<=next_Tj;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                end

                14:
                begin
                W14<=m_i;
                Wout67<=W10;
                Wout63<=W10^m_i;
                Tj<=next_Tj;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                end

                15:
                begin
                W15<=m_i;
                Wout67<=W11;
                Wout63<=W11^m_i;
                Tj<=next_Tj;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                end

                16,
                  17,
                    18,
                      19:
                      begin
                      Wout67<=W12;
                      Wout63<=W12^W16;
                      Tj<=next_Tj;
                      A<=TT1;
                      B<=A;
                      C<=next_C;
                      D<=C;
                      E<=next_E;
                      F<=E;
                      G<=next_G;
                      H<=G;
                      W0<=W1;
                      W1<=W2;
                      W2<=W3;
                      W3<=W4;
                      W4<=W5;
                      W5<=W6;
                      W6<=W7;
                      W7<=W8;
                      W8<=W9;
                      W9<=W10;
                      W10<=W11;
                      W11<=W12;
                      W12<=W13;
                      W13<=W14;
                      W14<=W15;
                      W15<=W16;
                      end

                20:
                begin
                Wout67<=W12;
                Wout63<=W12^W16;
                Tj<=32'h9d8a7a87;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                W0<=W1;
                W1<=W2;
                W2<=W3;
                W3<=W4;
                W4<=W5;
                W5<=W6;
                W6<=W7;
                W7<=W8;
                W8<=W9;
                W9<=W10;
                W10<=W11;
                W11<=W12;
                W12<=W13;
                W13<=W14;
                W14<=W15;
                W15<=W16;
                end

                21,
                  22,
                    23,
                      24,
                        25,
                          26,
                            27,
                              28,
                                29,
                                  30,
                                    31,
                                      32,
                                        33,
                                          34,
                                            35,
                                              36,
                                                37,
                                                  38,
                                                    39,
                                                      40,
                                                        41,
                                                          42,
                                                            43,
                                                              44,
                                                                45,
                                                                  46,
                                                                    47,
                                                                      48,
                                                                        49,
                                                                          50,
                                                                            51,
                                                                              52,
                                                                                53,
                                                                                  54,
                                                                                    55,
                                                                                      56,
                                                                                        57,
                                                                                          58,
                                                                                            59,
                                                                                              60,
                                                                                                61,
                                                                                                  62,
                                                                                                    63,
                                                                                                      64,
                                                                                                        65,
                                                                                                          66,
                                                                                                            67:
                                                                                                            begin
                                                                                                            Wout67<=W12;
                                                                                                            Wout63<=W12^W16;
                                                                                                            Tj<=next_Tj;
                                                                                                            A<=TT1;
                                                                                                            B<=A;
                                                                                                            C<=next_C;
                                                                                                            D<=C;
                                                                                                            E<=next_E;
                                                                                                            F<=E;
                                                                                                            G<=next_G;
                                                                                                            H<=G;
                                                                                                            W0<=W1;
                                                                                                            W1<=W2;
                                                                                                            W2<=W3;
                                                                                                            W3<=W4;
                                                                                                            W4<=W5;
                                                                                                            W5<=W6;
                                                                                                            W6<=W7;
                                                                                                            W7<=W8;
                                                                                                            W8<=W9;
                                                                                                            W9<=W10;
                                                                                                            W10<=W11;
                                                                                                            W11<=W12;
                                                                                                            W12<=W13;
                                                                                                            W13<=W14;
                                                                                                            W14<=W15;
                                                                                                            W15<=W16;
                                                                                                            end

                68:
                begin
                Wout67<=W12;
                Wout63<=W12^W16;
                Tj<=next_Tj;
                A<=TT1;
                B<=A;
                C<=next_C;
                D<=C;
                E<=next_E;
                F<=E;
                G<=next_G;
                H<=G;
                W0<=W1;
                W1<=W2;
                W2<=W3;
                W3<=W4;
                W4<=W5;
                W5<=W6;
                W6<=W7;
                W7<=W8;
                W8<=W9;
                W9<=W10;
                W10<=W11;
                W11<=W12;
                W12<=W13;
                W13<=W14;
                W14<=W15;
                W15<=W16;
                WOUT_0[255:224]<=TT1^WOUT_0[255:224];
                WOUT_0[223:192]<=A^WOUT_0[223:192];
                WOUT_0[191:160]<=next_C^WOUT_0[191:160];
                WOUT_0[159:128]<=C^WOUT_0[159:128];
                WOUT_0[127:96]<=next_E^WOUT_0[127:96];
                WOUT_0[95:64]<=E^WOUT_0[95:64];
                WOUT_0[63:32]<=next_G^WOUT_0[63:32];
                WOUT_0[31:0]<=G^WOUT_0[31:0];
                end

                69:
                begin
                A<=WOUT_0[255:224];
                B<=WOUT_0[223:192];
                C<=WOUT_0[191:160];
                D<=WOUT_0[159:128];
                E<=WOUT_0[127:96];
                F<=WOUT_0[95:64];
                G<=WOUT_0[63:32];
                H<=WOUT_0[31:0];
                wout=WOUT_0;
                end

                default:
                begin
                end

                endcase

        end
      else
                begin
          if(ctrl==3)
            begin
            Wout67<=0;
            Wout63<=0;
            A<=32'h7380166f;
            B<=32'h4914b2b9;
            C<=32'h172442d7;
            D<=32'hda8a0600;
            E<=32'ha96f30bc;
            F<=32'h163138aa;
            G<=32'he38dee4d;
            H<=32'hb0fb0e4e;
            Tj<=32'h79cc4519;
            WOUT_0[255:224]<=32'h7380166f;
            WOUT_0[223:192]<=32'h4914b2b9;
            WOUT_0[191:160]<=32'h172442d7;
            WOUT_0[159:128]<=32'hda8a0600;
            WOUT_0[127:96]<=32'ha96f30bc;
            WOUT_0[95:64]<=32'h163138aa;
            WOUT_0[63:32]<=32'he38dee4d;
            WOUT_0[31:0]<=32'hb0fb0e4e;
            end
                end
    end

end
endmodule
