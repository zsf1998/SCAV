#include "2.hpp"

void SM3_Controller::assign_count_plus()
{
	Wj_0=W0.read()^W1.read()^(W2.read().range(16,0),W3.read().range(31,17));
}

void SM3_Controller::assign_ctrl()
{
    Wj_0=W1.read()^(W2.read().range(16,0),W2.read().range(31,17))^W3.read();

}

void SM3_Controller::assign_ctr()
{
    Wj_0=(W0.read()&W1.read())|(W0.read()&W2.read())|(W1.read()&W2.read());
}

void SM3_Controller::always_block1()
{
    //if (neg_out.read()||neg_cnt.read())
    if (neg_out.read())
    	neg_out = pwm_rising_edge ? neg_cnt : neg_out;
    else
    	neg_out=neg_cnt.read();
    
}



