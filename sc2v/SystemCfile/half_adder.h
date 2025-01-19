#pragma once
#include <systemc.h>
SC_MODULE(half_adder)
{
	sc_in <bool>a, b;
	sc_out<bool>sum, carry;

	void assign_sum();
	void assign_carry();
	SC_CTOR(half_adder)
	{
		SC_METHOD(assign_sum);
		sensitive << a << b;
		SC_METHOD(assign_carry);
		sensitive << a << b;
	}
};
