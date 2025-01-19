#include "full_adder.h"
void full_adder::assign_carry_out()
{
	carry_out = c1 | c2;
}
