#include "systemc.h"

SC_MODULE(code_83)
{
	//port and signal declaration

	sc_signal <sc_uint<3> > func_code;
	sc_uint<3> function_func_code(sc_uint<8> func_func_din);
	sc_in <sc_uint<8> > din;
	sc_out <sc_uint<3> > dout;
	sc_signal <sc_uint<3> > d_out;

	// assign blocks
	void assign_d_out();
	void assign_dout();

	SC_CTOR(code_83)
	{
		SC_METHOD(assign_d_out);
		sensitive << din;
		SC_METHOD(assign_dout);
		sensitive << d_out;
		}
};