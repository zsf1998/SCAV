#include "systemc.h"

SC_MODULE(halfadder)
{
	//port and signal declaration

	sc_out <bool> sum;
	sc_out <bool> carry_out;
	sc_in <bool> a;
	sc_in <bool> b;

	// assign blocks
	void assign_sum();
	void assign_carry_out();

	SC_CTOR(halfadder)
	{
		SC_METHOD(assign_sum);
		sensitive << a << b;
		SC_METHOD(assign_carry_out);
		sensitive << a << b;
		}
};