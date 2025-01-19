#include "fulladder.hpp"


void fulladder::assign_carry_out()
{
	carry_out = c1.read() | c2.read();
}

