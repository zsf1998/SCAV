#include "systemc.h"

SC_MODULE(SM3_Controller)
{
	//port and signal declaration
	sc_uint<2> idle = 0b00;
	sc_uint<2> write = 0b01;
	sc_uint<2> encryption = 0b10;
	sc_uint<2> read = 0b11;

	sc_in <bool> clk, rst, W, R;
	sc_out <bool> finish;
	sc_out <sc_uint<7> > count_out;
	sc_out <sc_uint<2> > ctrl;
	sc_signal <sc_uint<2> > next_state, current_state;
	sc_signal <sc_uint<7> > count_plus;

	// assign blocks
	void assign_count_plus();
	void assign_ctrl();

	// always blocks
	void always_block1();
	void always_block2();
	void always_block3();

	SC_CTOR(SM3_Controller)
	{
		SC_METHOD(assign_count_plus);
		sensitive << count;
		SC_METHOD(assign_ctrl);
		sensitive << next_state;
		SC_METHOD(always_block1);
		sensitive << clk.pos() << rst.neg();
		SC_METHOD(always_block2);
		sensitive << clk.pos() << rst.neg();
		SC_METHOD(always_block3);
		sensitive << clk.pos() << rst.neg();
		}
};