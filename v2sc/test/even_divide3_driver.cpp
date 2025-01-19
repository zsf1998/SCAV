#include "even_divide3_driver.hpp"
void driver::test()
{
	while (true)
	{
		//输入激励信号
		wait(10,SC_NS);
	    wait(clk->posedge_event());
	    
	    sc_stop();
    }
}