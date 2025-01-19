#include "rom_ctrl.hpp"
#include "rom_ctrl_driver.hpp"

int sc_main(int argc, char* argv[]) {
	sc_signal<bool> sys_rst_n;
	sc_signal<bool> key1;
	sc_signal<bool> key2;
	sc_signal<sc_uint<8> > addr;

	//时钟声明：建立了时钟sys_clk，其周期为10ns，占空比为50%，在0ns后产生第一个时钟沿，第一个时钟沿处的初始值为false（即0）
	sc_clock sys_clk("sys_clk", 10, SC_NS, 0.5, 0, SC_NS, false);


	//实例化driver，创建对象u_driver
	driver u_driver("u_driver");
	u_driver.sys_rst_n(sys_rst_n);
	u_driver.key1(key1);
	u_driver.key2(key2);

	//实例化rom_ctrl，创建对象u_rom_ctrl
	rom_ctrl u_rom_ctrl("u_rom_ctrl");
	u_rom_ctrl.sys_clk(sys_clk);
	u_rom_ctrl.sys_rst_n(sys_rst_n);
	u_rom_ctrl.key1(key1);
	u_rom_ctrl.key2(key2);
	u_rom_ctrl.addr(addr);

	//生成vcd文件
	sc_trace_file* trace_file = sc_create_vcd_trace_file("rom_ctrl_vcd");

	//追踪rom_ctrl里的信号
	sc_trace<bool>(trace_file, u_rom_ctrl.sys_clk, "sys_clk");
	sc_trace<bool>(trace_file, u_rom_ctrl.sys_rst_n, "sys_rst_n");
	sc_trace<bool>(trace_file, u_rom_ctrl.key1, "key1");
	sc_trace<bool>(trace_file, u_rom_ctrl.key2, "key2");
	sc_trace<sc_uint<8> >(trace_file, u_rom_ctrl.addr, "addr");
	sc_trace<sc_uint<24> >(trace_file, u_rom_ctrl.cnt_200ms, "cnt_200ms");
	sc_trace<bool>(trace_file, u_rom_ctrl.key1_en, "key1_en");
	sc_trace<bool>(trace_file, u_rom_ctrl.key2_en, "key2_en");

	sc_start(10, SC_US);

	sc_close_vcd_trace_file(trace_file);

	return 0;
}