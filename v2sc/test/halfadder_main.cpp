#include "halfadder.hpp"
#include "halfadder_driver.hpp"

int sc_main(int argc, char* argv[]) {
	sc_signal<bool> sum;
	sc_signal<bool> carry_out;
	sc_signal<bool> a;
	sc_signal<bool> b;

	//时钟声明：建立了时钟，其周期为10ns，占空比为50%，在0ns后产生第一个时钟沿，第一个时钟沿处的初始值为false（即0）
	sc_clock ("", 10, SC_NS, 0.5, 0, SC_NS, false);


	//实例化driver，创建对象u_driver
	driver u_driver("u_driver");
	u_driver.a(a);
	u_driver.b(b);

	//实例化halfadder，创建对象u_halfadder
	halfadder u_halfadder("u_halfadder");
	u_halfadder.sum(sum);
	u_halfadder.carry_out(carry_out);
	u_halfadder.a(a);
	u_halfadder.b(b);

	//生成vcd文件
	sc_trace_file* trace_file = sc_create_vcd_trace_file("halfadder_vcd");

	//追踪halfadder里的信号
	sc_trace<bool>(trace_file, u_halfadder.sum, "sum");
	sc_trace<bool>(trace_file, u_halfadder.carry_out, "carry_out");
	sc_trace<bool>(trace_file, u_halfadder.a, "a");
	sc_trace<bool>(trace_file, u_halfadder.b, "b");

	sc_start(10, SC_US);

	sc_close_vcd_trace_file(trace_file);

	return 0;
}