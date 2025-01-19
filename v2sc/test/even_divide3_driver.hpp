#include <systemc.h>
SC_MODULE(driver) {
	sc_out <bool> rst;

	void test();
	
	SC_CTOR(driver)
	{
		SC_THREAD(test);

	}
};