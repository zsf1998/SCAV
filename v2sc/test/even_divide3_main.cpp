#include "even_divide3.hpp"
#include "even_divide3_driver.hpp"

int sc_main(int argc, char* argv[]) {
	sc_signal<bool> rst;
	sc_signal<bool> clk3;

	//时钟声明：建立了时钟clk，其周期为10ns，占空比为50%，在0ns后产生第一个时钟沿，第一个时钟沿处的初始值为false（即0）
	sc_clock clk("clk", 10, SC_NS, 0.5, 0, SC_NS, false);


	//实例化driver，创建对象u_driver
	driver u_driver("u_driver");
	u_driver.rst(rst);

	//实例化even_divide3，创建对象u_even_divide3
	even_divide3 u_even_divide3("u_even_divide3");
	u_even_divide3.clk(clk);
	u_even_divide3.rst(rst);
	u_even_divide3.clk3(clk3);

	//生成vcd文件
	sc_trace_file* trace_file = sc_create_vcd_trace_file("even_divide3_vcd");

	//追踪even_divide3里的信号
	sc_trace<bool>(trace_file, u_even_divide3.clk, "clk");
	sc_trace<bool>(trace_file, u_even_divide3.rst, "rst");
	sc_trace<bool>(trace_file, u_even_divide3.clk3, "clk3");
	sc_trace<sc_uint<2> >(trace_file, u_even_divide3.cnt, "cnt");
	sc_trace<bool>(trace_file, u_even_divide3.clk1, "clk1");
	sc_trace<bool>(trace_file, u_even_divide3.clk2, "clk2");

	sc_start(10, SC_US);

	sc_close_vcd_trace_file(trace_file);

	return 0;
}