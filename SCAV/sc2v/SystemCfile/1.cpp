#include "1.hpp"

void SM3_Controller::assign_count_plus()
{
    neg_out = pwm_rising_edge1 ? (sc_uint<1>)1 : neg_cnt;
    
}

void SM3_Controller::assign_ctrl()
{
    neg_out = (pwm_rising_edge.read()>1) ?  neg_cnt: (sc_uint<1>)1 ;

}

void SM3_Controller::assign_ctr()
{
    neg_out = (pwm_rising_edge.read()==10) ?  neg_cnt: (sc_uint<1>)1 ;
}

void SM3_Controller::assign_ct()
{
    neg_out = (pwm_rising_edge.read()>=10) ?  neg_cnt: neg_out;
}

void SM3_Controller::always_block1()
{
    neg_out = pwm_rising_edge1 ? neg_cnt : neg_out;
    neg_out = pwm_rising_edge1 ? (sc_uint<1>) 1 : neg_cnt;
    neg_out = (pwm_rising_edge.read()>1) ?  neg_cnt: (sc_uint<1>)1 ;
    neg_out = (pwm_rising_edge.read()==10) ?  neg_cnt: (sc_uint<1>)1 ;
    neg_out = (pwm_rising_edge.read()<=10) ?  (sc_uint<1>) 1 : neg_out;
}



