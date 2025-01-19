#include "halfadder.hpp"


void halfadder::assign_sum()
{
	sum = a.read() ^ b.read();
}


void halfadder::assign_carry_out()
{
	carry_out = a.read() & b.read();
}

