#include "systemc.h"

#define S0 0
#define S1 1
#define S2 2
#define S3 3
#define S4 4

SC_MODULE(moore_fsm)
{

	sc_in <bool> in;
	sc_in <bool> clk;
	sc_in <bool> rst;
	sc_out <bool> out;

	sc_signal <sc_uint<3> > current_state;
	sc_signal <sc_uint<3> > next_state;

	// always blocks	
	void always_combilogic_block1();
	void always_block1();

	void always_block2();

	SC_CTOR(moore_fsm)
	{		
		SC_METHOD(always_combilogic_block1);
		sensitive << next_state << in<<current_state;
		SC_METHOD(always_block1);
		sensitive << clk.pos() << rst.neg();

		SC_METHOD(always_block2);
		sensitive << clk.pos() << rst.neg();
		}
};
