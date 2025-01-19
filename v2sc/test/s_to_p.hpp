#include "systemc.h"

SC_MODULE(s_to_p)
{
	//port and signal declaration

	sc_in <bool> clk;
	sc_in <bool> rst_n;
	sc_in <bool> data_a, valid_a;
	sc_out <sc_uint<6> > data_b;
	sc_out <bool> valid_b;
	sc_out <bool> ready_a;
	sc_signal <sc_uint<6> > data_b1;
	sc_signal <sc_uint<4> > cnt;

	// assign blocks
	void assign_ready_a();

	// always blocks
	void always_block1();
	void always_block2();
	void always_block3();

	SC_CTOR(s_to_p)
	{
		SC_METHOD(assign_ready_a);
		sensitive;
		SC_METHOD(always_block1);
		sensitive << clk.pos() << rst_n.neg();
		SC_METHOD(always_block2);
		sensitive << clk.pos() << rst_n.neg();
		SC_METHOD(always_block3);
		sensitive << clk.pos() << rst_n.neg();
		}
};