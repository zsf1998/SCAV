#pragma once
#include"half_adder.h"
#include"half_adder.h"
SC_MODULE(full_adder)
{
	sc_in<bool>a, b, carry_in;
	sc_out<bool>sum, carry_out;
	sc_signal<bool>c1, c2, s1;


	void assign_carry_out();
	half_adder ha1;
	half_adder ha2;

	SC_CTOR(full_adder):ha1("ha1"),ha2("ha2")
	{
		
		ha1.a(a);
		ha1.b(b);
		ha1.sum(s1);
		ha1.carry(c1);

		
		ha2.a(s1);
		ha2.b(carry_in);
		ha2.sum(sum);
		ha2.carry(c2);



	//	ha2_ptr = new half_adder("ha2");
	//	(*ha2_ptr)(s1, carry_in, sum, c2);

		SC_METHOD (assign_carry_out);
		sensitive << c1 << c2;

	}

};
