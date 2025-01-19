#include "systemc.h"

SC_MODULE(CompressExtend)
{
	//port and signal declaration

	sc_in <bool> clk, rst;
	sc_in <bool> finish;
	sc_in <sc_uint<2> > ctrl;
	sc_in <sc_uint<32> > m_i;
	sc_in <sc_uint<7> > Round;
	sc_out <sc_biguint<256> > wout;
	sc_signal <sc_biguint<256> > WOUT_0;
	sc_signal <sc_uint<32> > W0, W1, W2, W3, W4, W5, W6, W7, W8, W9, W10, W11, W12, W13, W14, W15, Wout67, Wout63, Tj;
	sc_signal <sc_uint<32> > A, B, C, D, E, F, G, H;
	sc_signal <sc_uint<32> > Wj_0_out, W16;
	sc_signal <sc_uint<32> > SS1_0, SS2, TT1, TT2, FF, GG, next_Tj, next_C, next_E, next_G;
	sc_signal <sc_uint<32> > TT1_0, TT1_1, TT2_0, TT2_1, FF_0, FF_1, GG_0, GG_1;
	sc_biguint<256> var_WOUT_0;
	sc_biguint<256> var_wout;

	// assign blocks
	void assign_Wj_0();
	void assign_W16();
	void assign_SS1_0();
	void assign_SS1();
	void assign_SS2();
	void assign_FF_0();
	void assign_FF_1();
	void assign_GG_0();
	void assign_GG_1();
	void assign_FF();
	void assign_GG();
	void assign_TT1();
	void assign_TT2();
	void assign_next_Tj();
	void assign_next_C();
	void assign_next_E();
	void assign_next_G();

	// always blocks
	void always_block1();

	SC_CTOR(CompressExtend)
	{
		SC_METHOD(assign_Wj_0);
		sensitive << W0 << W7 << W13;
		SC_METHOD(assign_W16);
		sensitive << Wj_0 << W3 << W10;
		SC_METHOD(assign_SS1_0);
		sensitive << A << E << Tj;
		SC_METHOD(assign_SS1);
		sensitive << SS1_0;
		SC_METHOD(assign_SS2);
		sensitive << SS1 << A;
		SC_METHOD(assign_FF_0);
		sensitive << A << B << C;
		SC_METHOD(assign_FF_1);
		sensitive << A << B << C;
		SC_METHOD(assign_GG_0);
		sensitive << E << F << G;
		SC_METHOD(assign_GG_1);
		sensitive << E << F << G;
		SC_METHOD(assign_FF);
		sensitive << Round << FF_0 << FF_1;
		SC_METHOD(assign_GG);
		sensitive << Round << GG_0 << GG_1;
		SC_METHOD(assign_TT1);
		sensitive << FF << D << SS2 << Wout63;
		SC_METHOD(assign_TT2);
		sensitive << GG << H << SS1 << Wout67;
		SC_METHOD(assign_next_Tj);
		sensitive << Tj;
		SC_METHOD(assign_next_C);
		sensitive << B;
		SC_METHOD(assign_next_E);
		sensitive << TT2;
		SC_METHOD(assign_next_G);
		sensitive << F;
		SC_METHOD(always_block1);
		sensitive << clk.pos() << rst.neg();
		}
};