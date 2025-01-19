import re
import sys

input_file = '%s' % sys.argv[1]
module_name = '%s' % sys.argv[1]

# input_file = "test3"

txt = open('test/%s_txt.txt' % input_file)
sysc = open('test/%s_driver.cpp' % input_file, 'w+')
sysh = open('test/%s_driver.hpp' % input_file, 'w+')
sys = open('test/%s_main.cpp' % input_file, 'w+')

instance_driver_content = ''
instance_module_content = ''
trace_content = ''
clk = ''
port_content_list = []


regx_in = re.compile("sc_in ((<.*>) (.*));")
regx_out = re.compile("sc_out ((<.*>) (.*));")
regx_signal = re.compile("sc_signal ((<.*>) (.*));")

sysh.write("#include <systemc.h>\n")
sysh.write("SC_MODULE(driver) {\n")

sysc.write('#include "%s_driver.hpp"' % module_name)
sysc.write(
"""
void driver::test()
{
	while (true)
	{
		//输入激励信号
		wait(10,SC_NS);
	    wait(clk->posedge_event());
	    
	    sc_stop();
    }
}"""
)

sys.write('#include "%s.hpp"\n#include "%s_driver.hpp"\n' % (module_name, module_name))
sys.write("\nint sc_main(int argc, char* argv[]) {\n")

instance_driver_content = '\n\t//实例化driver，创建对象u_driver\n\tdriver u_driver("u_driver");\n'
instance_module_content = '\n\t//实例化%s，创建对象u_%s\n\t%s u_%s("u_%s");\n' % (module_name, module_name, module_name, module_name, module_name)
trace_content = '\n\t//追踪%s里的信号\n' % module_name


def module_separate(group_3):
    content = ""
    if ',' in group_3:
        new_group_3 = group_3.split(",")
        # print(new_group_3)
        for i in range(len(new_group_3)):
            content = content + '\tu_%s.%s("%s");\n' % (module_name, new_group_3[i], new_group_3[i])
    return content

def driver_separate(group_3):
    content = ""
    if ',' in group_3:
        new_group_3 = group_3.split(",")
        for i in range(len(new_group_3)):
            if ("clk" or "CLK") in new_group_3[i]:
                content = ''
            else:
                content = content + '\tu_driver.%s("%s");\n' % (new_group_3[i], new_group_3[i])
    return content

def trace_separate(group_2,group_3):
    content = ""
    if ',' in group_3:
        new_group_3 = group_3.split(",")
        # print(new_group_3)
        for i in range(len(new_group_3)):
            content = content+'\tsc_trace%s(trace_file, u_%s.%s, "%s"); \n' % (group_2, module_name, new_group_3[i], new_group_3[i])
    return content

def clk_separate(group_2,group_3):
    driver_content = ""
    main_signal_content = ''

    if ',' in group_3:
        new_group_3 = group_3.split(",")
        for i in range(len(new_group_3)):
            if ("clk" or "CLK") in new_group_3[i]:
                clk = '%s' % new_group_3[i]
            else:
                driver_content = driver_content + '\tsc_out %s %s;\n' % (group_2, new_group_3[i])
                main_signal_content = main_signal_content + '\tsc_signal %s %s;\n' % (group_2, new_group_3[i])
    else:
        sysh.write("")
        sys.write("")
    return clk, driver_content, main_signal_content



for line in txt.readlines():
    # print(line)
    if regx_in.search(line):
        regx_in_obj = regx_in.search(line)
        # print(regx_in_obj.group(3))
        if "clk" in regx_in_obj.group(3) or "CLK" in regx_in_obj.group(3):
            if "," in regx_in_obj.group(3):
                clk_port = clk_separate(regx_in_obj.group(2), regx_in_obj.group(3))
                clk = clk_port[0]
                sysh.write(clk_port[1])
                sys.write(clk_port[2])
            else:
                clk = regx_in_obj.group(3)
        else:
            sysh.write("\tsc_out %s;\n" % regx_in_obj.group(1))
            sys.write("\tsc_signal%s;\n" % regx_in_obj.group(1))


        if ","in regx_in_obj.group(3):
            instance_module_content = instance_module_content + module_separate(regx_in_obj.group(3))
            instance_driver_content = instance_driver_content + driver_separate(regx_in_obj.group(3))
            trace_content = trace_content + trace_separate(regx_in_obj.group(2), regx_in_obj.group(3))
        else:
            if "clk" in regx_in_obj.group(3) or "CLK" in regx_in_obj.group(3):
                instance_driver_content = instance_driver_content
            else:
                instance_driver_content = instance_driver_content + '\tu_driver.%s(%s);\n' % (regx_in_obj.group(3), regx_in_obj.group(3))

            instance_module_content = instance_module_content + '\tu_%s.%s(%s);\n' % (module_name, regx_in_obj.group(3), regx_in_obj.group(3))
            trace_content = trace_content + '\tsc_trace%s(trace_file, u_%s.%s, "%s");\n' % (regx_in_obj.group(2), module_name, regx_in_obj.group(3), regx_in_obj.group(3))


    elif regx_out.search(line):
        regx_out_obj = regx_out.search(line)
        sys.write("\tsc_signal%s;\n" % regx_out_obj.group(1))
        if "," in regx_out_obj.group(3):
            instance_module_content=instance_module_content + module_separate(regx_out_obj.group(3))
            trace_content = trace_content + trace_separate(regx_out_obj.group(2),regx_out_obj.group(3))
        else:
            instance_module_content = instance_module_content + '\tu_%s.%s(%s);\n' % (module_name, regx_out_obj.group(3), regx_out_obj.group(3))
            trace_content = trace_content + '\tsc_trace%s(trace_file, u_%s.%s, "%s");\n' % (regx_out_obj.group(2), module_name, regx_out_obj.group(3), regx_out_obj.group(3))

    elif regx_signal.search(line):
        regx_signal_obj = regx_signal.search(line)
        if "," in regx_signal_obj.group(3):
            trace_content = trace_content + trace_separate(regx_signal_obj.group(2),regx_signal_obj.group(3))
        else:
            trace_content = trace_content + '\tsc_trace%s(trace_file, u_%s.%s, "%s");\n' % (regx_signal_obj.group(2), module_name, regx_signal_obj.group(3), regx_signal_obj.group(3))

#时钟信号输出
sys.write("\n\t//时钟声明：建立了时钟%s，其周期为10ns，" % clk)
sys.write("占空比为50%，在0ns后产生第一个时钟沿，第一个时钟沿处的初始值为false（即0）")
sys.write('\n\tsc_clock %s("%s", 10, SC_NS, 0.5, 0, SC_NS, false);\n\n' % (clk, clk))

sys.write(instance_driver_content)
sys.write(instance_module_content)

sys.write("\n\t//生成vcd文件")
sys.write('\n\tsc_trace_file* trace_file = sc_create_vcd_trace_file("%s_vcd");\n' % module_name)

sys.write(trace_content)


sys.write("\n\tsc_start(10, SC_US);\n")
sys.write("\n\tsc_close_vcd_trace_file(trace_file);\n")
sys.write("\n\treturn 0;\n}")
sysh.write("""\n	void test();
	
	SC_CTOR(driver)
	{
		SC_THREAD(test);

	}
};"""
)

# sysh.seek(0)
# print(sysh.read())
# sysc.seek(0)
# print(sysc.read())
sys.seek(0)
print(sys.read())
