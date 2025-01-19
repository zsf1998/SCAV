#include <systemc.h>
SC_MODULE(driver) {
	sc_out <bool> a;
	sc_out <bool> b;

	void test();
	
	SC_CTOR(driver)
	{
		SC_THREAD(test);

	}
};