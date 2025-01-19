#include "systemc.h"

SC_MODULE(fulladder)
{
	//port and signal declaration

	//instance module declaration
	halfadder ha1;
	halfadder ha2;

	sc_in <bool> a;
	sc_in <bool> b;
	sc_in <bool> carry_in;
	sc_out <bool> sum;
	sc_out <bool> carry_out;
	sc_signal <bool> s1;
	sc_signal <bool> c1;
c2;
}


	// assign blocks
	void assign_carry_out();

	SC_CTOR(fulladder):
		ha1("ha1")
		, ha2("ha2")

	{
		ha1.a(a);
		ha1.b(b);
		ha1.sum(s1);
		ha1.carry(c1);

		ha2.a(s1);
		ha2.b(carry_in);
		ha2.sum(sum);
		ha2.carry(c2);

		SC_METHOD(assign_carry_out);
		sensitive << c1 << c2;
		}
};