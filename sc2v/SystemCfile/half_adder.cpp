#include "half_adder.h"
void half_adder::assign_sum()
{
	sum = a.read() ^ b.read();
	
}

void half_adder::assign_carry()
{
	carry = a.read() & b.read();
}
