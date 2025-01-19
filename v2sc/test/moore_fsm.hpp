#include "systemc.h"

SC_MODULE(moore_fsm)
{
	//port and signal declaration
	sc_uint<1> S0 = 0;
	sc_uint<1> S1 = 1;
	sc_uint<1> S2 = 2;
	sc_uint<1> S3 = 3;
	sc_uint<1> S4 = 4;
	sc_in <bool> in;
	sc_in <bool> clk;
	sc_in <bool> rst;
	sc_out <bool> out;
	sc_signal <sc_uint<3> > current_state;
	sc_signal <sc_uint<3> > next_state;

	// always blocks
	void always_block1();
	void always_combilogic_block2();
	void always_block3();

	SC_CTOR(moore_fsm)
	{
		SC_METHOD(always_block1);
		sensitive << clk.pos() << rst.neg();
		SC_METHOD(always_combilogic_block2);
		sensitive << next_state << S0;
		SC_METHOD(always_block3);
		sensitive << clk.pos() << rst.neg();
		}
};