#include "systemc.h"

SC_MODULE(even_divide3)
{
	//port and signal declaration
	sc_in <bool> clk;
	sc_in <bool> rst;
	sc_out <bool> clk3;
	sc_signal <sc_uint<2> > cnt;
	sc_signal <bool> clk1;
	sc_signal <bool> clk2;

	// always blocks
	void always_block1();
	void always_block2();
	void always_block3();
	void assign_clk3();


	// assign blocks


	SC_CTOR(even_divide3)
	{
		SC_METHOD(assign_clk3);
		sensitive << clk1<< clk2;
		SC_METHOD(always_block1);
		sensitive << clk.pos() << rst.neg();
		SC_METHOD(always_block2);
		sensitive << clk.pos() << rst.neg();
		SC_METHOD(always_block3);
		sensitive << clk.neg() << rst.neg();

		}
};
