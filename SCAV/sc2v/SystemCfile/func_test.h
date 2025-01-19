#pragma once
#include "systemc.h"
SC_MODULE(code_83)
{
	//port_list_right declaration
	sc_in <sc_uint<8> > din;
	sc_out <sc_uint<3> > dout;
	sc_signal <sc_uint<3> >  out;
	sc_signal <sc_uint<3> > func_code;

	sc_uint<3> function_code( sc_uint<8>  func_din);

	// assign blocks
	void assign_out();
	void assign_dout();


	SC_CTOR(code_83)
	{
		SC_METHOD(assign_out);
		sensitive << din;
		SC_METHOD(assign_dout);
		sensitive << out;
	}
};