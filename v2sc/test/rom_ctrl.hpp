#include "systemc.h"

SC_MODULE(rom_ctrl)
{
	//port and signal declaration
	int rom_ctrl_CNT_MAX = 9_999_999;
	sc_in <bool> sys_clk;
	sc_in <bool> sys_rst_n;
	sc_in <bool> key1;
	sc_in <bool> key2;
	sc_out <sc_uint<8> > addr;
	sc_signal <sc_uint<24> > cnt_200ms;
	sc_signal <bool> key1_en;
	sc_signal <bool> key2_en;

	// always blocks
	void always_block1();
	void always_block2();
	void always_block3();
	void always_block4();

	SC_CTOR(rom_ctrl)
	{
		SC_METHOD(always_block1);
		sensitive << sys_clk.pos() << sys_rst_n.neg();
		SC_METHOD(always_block2);
		sensitive << sys_clk.pos() << sys_rst_n.neg();
		SC_METHOD(always_block3);
		sensitive << sys_clk.pos() << sys_rst_n.neg();
		SC_METHOD(always_block4);
		sensitive << sys_clk.pos() << sys_rst_n.neg();
		}
};