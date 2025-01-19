#include <systemc.h>
SC_MODULE(driver) {
	sc_out <bool> sys_rst_n;
	sc_out <bool> key1;
	sc_out <bool> key2;

	void test();
	
	SC_CTOR(driver)
	{
		SC_THREAD(test);

	}
};