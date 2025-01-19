#pragma once
#pragma once
#include "systemc.h"
#define idle  0b00                // idle state, no operation
#define write_  0b01	           // write register 
#define encryption  0b10		   // encryption only
#define read_  0b11		    	   // read register

SC_MODULE(SM3_Controller)
{
	sc_in_clk clk;
	sc_in<bool> rst, W, R;
	sc_out<bool> finish;

	sc_out<sc_uint<7> > count_out;    // calculat the times of extend&compress&writeresult 
	sc_out<sc_uint<2> > ctrl;

	sc_signal<sc_uint<7> > count;
	sc_signal<sc_uint<2> > next_state, current_state;
	sc_signal<sc_uint<7> > count_plus;
	sc_signal<sc_uint<1> >  neg_out, neg_cnt;
	sc_signal<sc_uint<1> > pwm_rising_edge;
	sc_signal<bool > pwm_rising_edge1;
	sc_signal<sc_uint<32> > FF,FF_0,FF_1;
	


	void assign_count_plus();
	void assign_ctrl();
	void assign_ctr();
	void assign_ct();
	void always_block1(); //current_state reg

	//output logic
	// at each state , we can output signals



	SC_CTOR(SM3_Controller)
	{
		SC_METHOD(assign_count_plus);
		sensitive << pwm_rising_edge << neg_cnt;
		SC_METHOD(assign_ctrl);
		sensitive << neg_out << pwm_rising_edge << neg_cnt;
		SC_METHOD(assign_ctr);
		sensitive << count << FF_0<< FF_1;
		SC_METHOD(assign_ct);
		sensitive << count << FF_0<< FF_1;
		SC_METHOD(always_block1);
		sensitive << clk.pos() << rst.pos();

	}

};
