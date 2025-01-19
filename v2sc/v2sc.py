import re
import time
import os
import sys

#input_file = "code_83"
# time_start = time.time()   #测试c程序运行时间

input_file = '%s' % sys.argv[1]

txt = open('test/%s_ast.txt' % input_file)
sysc = open('test/%s.cpp' % input_file, 'w+')
sysh = open('test/%s.hpp' % input_file, 'w+')
sysh_txt = open('test/%s_txt.txt' % input_file, 'w+')

#变量、列表初始化
module_name = ''               #定义模块名
function_name = ''             #定义函数名
instance_name = ''             #定义实例化名称
statement_spacenu_num = ''     #每个语句前的空格数
intconst_num = ''              #IntConst前的空格数
symbol = ''                    #整句语句符号位定义
brackets_symbol = ''           #括号里的符号
line_content = ''              #中间变量
content = ''                   #中间变量
content1 = ''                  #中间变量
content2 = ''                  #中间变量
var1 = ''                      #中间变量
var2 = ''                      #中间变量
var3 = ''                      #中间变量
port_content = ''             #存储端口信号等内容
sign = ''                      #中间变量
else_sign = ''                 #判断是否有else
sentence_sign = ''             #assign和always的标志，用于判断identified的内容属于什么类型
cond_sign = ''                 #条件判断操作符的标志
port_sign = ''                 #用于判断参数是宏定义还是局部定义：'exist'表示局部定义，空表示宏定义
read_state = ''                #用于判断AST文件读取完毕
case_intconst = ''             #用于判断case部分default
casestatement = ''             #用于判断是否含有case语句，是的话需要在结束部分添加一个'}'
function_line_content = ''     #存储function的函数名和位宽等信息
biguint_content = ''           #存储biguint的变量
port_left = ''                 #存储等号左边的信号变量
lvalue_selection_port = ''     #左值端口的中间变量
hpp_port_content = ''          #存储hpp内端口信号定义部分
hpp_assign_content = ''        #存储hpp内assign声明部分
hpp_always_content = ''        #存储hpp内always声明部分
port_left_type = ''            #存储左值数据类型
port_right_type = ''           #存储右值数据类型
# port_left_type_content = ''    #存储左值数据类型

i = 0
j = 0
data_type = 0                  #判断括号里的数据类型，1为带位宽类型，2为判断类型(即（）？：),3括号中端口含有非~,4端口位宽为[]形式,5非号为!形式,6为与&&
portdefine_type = 0            #定义端口的类型：1是input，2是inout,3是output，4是reg和wire
sentence_type = 0              #判断语句类型，1为if语句，2为读取值直接赋端口,3为case语句,4为switch
value_type = 0                 #判断identifier读取的端口位置，1为等式左边端口，2为等式右边端口，0为无等式端口
always_type = 0                #判断always是时序逻辑（1）还是组合逻辑（2）

linenum = 1                    #存储上一行的行数
port_num = 0                   #统计端口数目
symbol_num = 0                 #统计符号数目
bracket_port_num = 0           #统计括号里的端口数
unot_num = 0                   #统计unot的个数
assign_num = 0                 #统计assign的个数
always_num = 0                 #统计always的个数
case_num = 0                   #统计case的个数
instance_num = 0               #统计实例化对象的个数
ifstatement_num = 0            #统计ifstatement的个数
assign_sumnum = 0              #assign的总数
always_sumnum = 0              #always的总数
sens_num = 0                   #上升沿下降沿的个数
and_spacenum = 0               #And前的空格数，如果与最后一个And空格数相同的identified，既为并列关系
space_num = 0                  #空格数，每多一个层级增加4个
brackets_position = 0          #大括号位于port数组中的位置
block_space_num = 0            #存储block的空格数
cond_block_num = 0             #存储条件选择符号前的空格数
func_identifier_num = 0        #计算function调用里identifier的个数，以判断哪个是函数名（用此判断是因为有可能出现情况function的定义在后面，而function调用在前面使用）
ifelse_sign = 0                #判断if是否为else-if
instance_num = 0               #统计实例化模块的个数
partselect_num = 0             #统计partselect的个数，用以判断需要添加多少个'，'
and_symbol_num = 0             #统计and的个数
nonblockingsubstitution_num = 0  #统计if内nonblockingsubstitution的个数
# block_current_num = 0          #当前blcok的空格数
# bracket_firstport_num = 0      #存储括号内读到的第一个端口前的空格数
# ifstatement_space_num = 0      #存储ifstatement的空格数
# ifstatement_current_num = 0    #当前ifstatement的空格数
# unot_space_num = 0             #存储~unot之前的空格数，判断identifier读取到的端口是否为并列关系
plus_identifier_num = 0

port_list_width = []           #存储width位宽的列表，用于计算width位宽
port_list_right = []           #等号右端口存储的列表
block_list_level = []          #统计不同层次的block的列表
block_list_if = []             #存储if的第一个block空格数的列表
ifstatement_list_if = []       #存储ifstatement的空格数的列表
block_list_case = []           #存储第一个case的第一个block空格数的列表
cond_list = []                 #存储条件选择操作符中的多元操作的列表
instance_module_name_list = []        #存储实例化模块的名称
instance_object_name_list = []         #存储实例化对象名称的列表
paramarg_list = []             #存储实例化的参数
paramarg_content_list = []     #存储实例化参数赋值的内容
# sysh_content = []
symbol_list = []                #存储整句语句的连接符号
brackets_symbol_list = []       #存储语句中的连接符号

names = locals()               #定义动态变量


def brackrts(brackets_symbol_list,brackets_position,i,bracket_port_num,port_list_right):            #括号内容转译函数
    # i = 0
    if partselect_num != 0:
        bracket_port_num = partselect_num
    else:
        pass
    if bracket_port_num == 1:
        var = port_list_right[brackets_position]
        del port_list_right[brackets_position]
        if brackets_symbol_list == []:
            content = '%s' % var
        else:
            content = '%s %s' % (var, brackets_symbol_list[i])
        port_list_right.append(content)
    else:
        while bracket_port_num > 0:
            if i == 0:
                var = port_list_right[brackets_position]
                del port_list_right[brackets_position]
                if brackets_symbol_list == []:
                    if symbol == "":
                        content = '%s ' % var
                    else:
                        content = '%s %s ' % (var, symbol)
                else:
                    content = '(%s %s ' % (var, brackets_symbol_list[i])  # 读取括号中第一个
                i += 1
                bracket_port_num -= 1
            else:
                if bracket_port_num > 1:
                    var = port_list_right[brackets_position]
                    del port_list_right[brackets_position]
                    if brackets_symbol_list == []:
                        content1 = '%s  ' % var
                    else:
                        content1 = '%s %s ' % (var, brackets_symbol_list[i])  # 中间变量无实际作用
                    content = content + content1
                    i += 1
                    bracket_port_num -= 1
                else:
                    var = port_list_right[brackets_position]
                    if brackets_symbol_list == []:
                        content1 = '%s' % var  # 读取括号最后一个端口
                    else:
                        content1 = '%s)' % var  # 读取括号最后一个端口
                    content = content + content1
                    port_list_right[brackets_position] = content
                    i, bracket_port_num = 0, 0
                    content, content1 = '', ''
    return port_list_right

def input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right, line_content):                #整句输出
    if bracket_port_num != 0:
        port_list_right = brackrts(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right)
    content = ''  # 大括号里的端口输入就此为止
    biguint_content = ''
    if port_list_right != []:
        port_num = len(port_list_right)
        while port_num > 1:
            if portdefine_type == 'input':     #input类型
                if data_type == 1:
                    width = int(port_list_width[0]) - int(port_list_width[1]) + 1   #计算位宽长度
                    if width < 64:
                        line_content = '\tsc_in <sc_uint<%d> > ' % width
                        content1 = '%s, ' % port_list_right[i]
                    else:
                        line_content = '\tsc_in <sc_biguint<%d> > ' % width
                        content1 = '%s, ' % port_list_right[i]
                else:  #没有位宽
                    line_content = '\tsc_in <bool> '
                    content1 = '%s, ' % port_list_right[i]
            elif portdefine_type == 'inout':     #inout类型
                if data_type == 1:
                    width = int(port_list_width[0]) - int(port_list_width[1]) + 1   #计算位宽长度
                    if width < 64:
                        line_content = '\tsc_inout <sc_uint<%d> > ' % width
                        content1 = '%s, ' % port_list_right[i]
                    else:
                        line_content = '\tsc_inout <sc_biguint<%d> > ' % width
                        content1 = '%s, ' % port_list_right[i]
                else:  #没有位宽
                    line_content = '\tsc_inout <bool> '
                    content1 = '%s, ' % port_list_right[i]
            elif portdefine_type == 'output':     #output类型
                if data_type == 1:
                    width = int(port_list_width[0]) - int(port_list_width[1]) + 1   #计算位宽长度
                    if width < 64:
                        line_content = '\tsc_out <sc_uint<%d> > ' % width
                        content1 = '%s, ' % port_list_right[i]
                    else:
                        line_content = '\tsc_out <sc_biguint<%d> > ' % width
                        content1 = '%s, ' % port_list_right[i]
                else:  #没有位宽
                    line_content = '\tsc_out <bool> '
                    content1 = '%s, ' % port_list_right[i]
            elif portdefine_type == 'signal':     #reg和wire类型
                if data_type == 1:
                    width = int(port_list_width[0]) - int(port_list_width[1]) + 1   #计算位宽长度
                    if width < 64:
                        line_content = '\tsc_signal <sc_uint<%d> > ' % width
                        content1 = '%s, ' % port_list_right[i]
                    else:
                        line_content = '\tsc_signal <sc_biguint<%d> > ' % width
                        content1 = '%s, ' % port_list_right[i]
                else:  #没有位宽
                    if i == 0:
                        content = '\tsc_signal <bool> '
                        content1 = '%s, ' % port_list_right[i]
                    else:
                        content1 = '%s, ' % port_list_right[i]
            elif portdefine_type == 'parameter':
                line_content = '\tsc_uint %s' % port_list_right[i]
            elif symbol == '()':   #调用function函数
                content1 = 'function_%s' % function_name
            else:
                if symbol_list == []:
                    content1 = '%s' % port_list_right[i]
                else:
                    if data_type == 2:  #条件选择语句
                        content1 = '%s' % port_list_right[i]
                    else:
                        content1 = '%s %s ' % (port_list_right[i], symbol_list[i])
            i += 1
            port_num -= 1
            content = content + content1
        if port_num == 1:  # 让第一个assign不输出内容，理论上如果完整verilog函数的话，应该不需要这一句
            if portdefine_type == 'input':     #input类型
                if i != 0:
                    if data_type == 1:
                        width = int(port_list_width[0]) - int(port_list_width[1]) + 1
                        if width < 64:
                            content1 = '%s;\n' % port_list_right[i]
                        else:
                            content1 = '%s;\n' % port_list_right[i]
                    else:
                        content1 = '%s;\n' % port_list_right[i]
                else:
                    if data_type == 1:
                        width = int(port_list_width[0]) - int(port_list_width[1]) + 1
                        if width < 64:
                            content1 = '\tsc_in <sc_uint<%d> > %s;\n' % (width, port_list_right[i])
                        else:
                            content1 = '\tsc_in <sc_biguint<%d> > %s;\n' % (width, port_list_right[i])
                    else:
                        content1 = '\tsc_in <bool> %s;\n' % port_list_right[i]
                content = content + content1
            elif portdefine_type == 'inout':  # inout类型
                if i != 0:
                    if data_type == 1:
                        width = int(port_list_width[0]) - int(port_list_width[1]) + 1
                        if width < 64:
                            content1 = '%s;\n' % port_list_right[i]
                        else:
                            content1 = '%s;\n' % port_list_right[i]
                    else:
                        content1 = '%s;\n' % port_list_right[i]
                else:
                    if data_type == 1:
                        width = int(port_list_width[0]) - int(port_list_width[1]) + 1
                        if width < 64:
                            content1 = '\tsc_inout <sc_uint<%d> > %s;\n' % (width, port_list_right[i])
                        else:
                            content1 = '\tsc_inout <sc_biguint<%d> > %s;\n' % (width, port_list_right[i])
                    else:
                        content1 = '\tsc_inout <bool> %s;\n' % port_list_right[i]
                content = content + content1
            elif portdefine_type == 'output':  # output类型
                if i != 0:
                    if data_type == 1:
                        width = int(port_list_width[0]) - int(port_list_width[1]) + 1
                        if width < 64:
                            content1 = '%s;\n' % port_list_right[i]
                        else:
                            content1 = '%s;\n' % port_list_right[i]
                    else:
                        content1 = '%s;\n' % port_list_right[i]
                else:
                    if data_type == 1:
                        if int(port_list_width[0]) > int(port_list_width[1]):
                            width = int(port_list_width[0]) - int(port_list_width[1]) + 1
                        else:
                            width = int(port_list_width[1]) - int(port_list_width[0]) + 1
                        if width < 64:
                            content1 = '\tsc_out <sc_uint<%d> > %s;\n' % (width, port_list_right[i])
                        else:
                            content1 = '\tsc_out <sc_biguint<%d> > %s;\n' % (width, port_list_right[i])
                    else:
                        content1 = '\tsc_out <bool> %s;\n' % port_list_right[i]
                content = content + content1
            elif portdefine_type == 'signal':     #reg和wire类型
                if i != 0:
                    if data_type == 1:
                        width = int(port_list_width[0]) - int(port_list_width[1]) + 1
                        if width < 64:
                            content1 = '%s;\n' % port_list_right[i]
                        else:
                            content1 = '%s;\n' % port_list_right[i]
                    else:
                        content1 = '%s;\n' % port_list_right[i]
                else:
                    if data_type == 1:
                        width = int(port_list_width[0]) - int(port_list_width[1]) + 1
                        if width < 64:
                            content1 = '\tsc_signal <sc_uint<%d> > %s;\n' % (width, port_list_right[i])
                        else:
                            content1 = '\tsc_signal <sc_biguint<%d> > %s;\n' % (width, port_list_right[i])
                    else:
                        content1 = '\tsc_signal <bool> %s;\n' % port_list_right[i]
                content = content + content1
            elif portdefine_type == 'integer':     #integer类型
                width = int(port_list_width[0]) - int(port_list_width[1]) + 1
                content1 = '\tsc_signal <sc_int<%s> > %s;\n' % (width, port_list_right[i])
                content = content + content1
            elif portdefine_type == 'uint':
                width = int(port_list_width[0]) - int(port_list_width[1]) + 1
                content1 = '(sc_uint<%d> func_%s)' % (width, port_list_right[i])
                content = content + content1
                if sentence_type != 4:
                    sysh.write('(sc_uint<%d> func_%s);\n' % (width, port_list_right[i]))
            elif portdefine_type == 'parameter':      #parameter类型
                sysh.write('')
            elif sentence_type == 1:    #if语句
                content = port_list_right[i]
            elif sign == 'uadnd' or sign == 'unand' or sign == 'uor' or sign == 'unor' or sign == 'uxor' or sign == 'uxnor':  #归约操作符处理
                content1 = '%s %s;\n' % (symbol, port_list_right[i])
                content = content + content1
            elif symbol == '()':  #调用fucntion函数
                content1 = '(%s.read());\n}\n' % port_list_right[i]
                content = content + content1
            else:
                if else_sign == 'else':
                    content1 = '%s;\n' % port_list_right[i]
                elif lvalue_selection_port != '':
                    content1 = "%s;\n\t%s = %s;\n}\n" % (port_list_right[i], port_left, lvalue_selection_port)
                else:
                    if read_state == 'end':
                        if sentence_sign == 'always':
                            content1 = '%s;\n' % port_list_right[i]
                        elif sentence_sign == 'assign':
                            content1 = '%s;\n}\n\n' % port_list_right[i]
                    else:
                        content1 = '%s;\n}\n\n' % port_list_right[i]
                content = content + content1  # 端口输出就此为止
    line_content = line_content + content
    return line_content

#头文件添加
sysh.write('#include "systemc.h"\n\n')
sysc.write('#include "%s.hpp"\n\n' % input_file)

#ast逐行读取，获取所需数据并进行处理
line = txt.readline()
while line:
    #端口名处理
    if 'ModuleDef' in line:      #提取模块名
        var = re.search(': (\w+) ',line)
        module_name = var.group(1)
        sysh.write('SC_MODULE(%s)\n' % module_name)
        sysh.write('{\n\t//port and signal declaration\n')
        line = txt.readline()

    # 实例化模块
    elif 'InstanceList' in line:   #提取实例化模块名称
        else_sign = ''
        if sentence_sign == 'always' or sentence_sign == 'assign':
            line_content = input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right,line_content)
            sysc.write(line_content)
        sentence_type, value_type, portdefine_type = 0, 0, 0
        instance_name = ''
        paramarg_list = []            # 清空数组，避免影响下一个有实例化参数赋值的情况
        instance_num += 1
        var = re.search(': (\w+) ', line)
        instance_name = var.group(1)
        instance_module_name_list.append(instance_name)
        line = txt.readline()
    elif 'Instance:' in line:    #提取实例化对象的名称
        # sign = 'instance'
        var = re.search(': (\w+),', line)
        content = var.group(1)
        instance_object_name_list.append(content)
        # instance_num += 1
        names['instance' + str(instance_num)] = []     #存储实例化对象的端口内容
        names['portarg' + str(instance_num)] = []      #存储实例化对象的端口参数
        if instance_num == 1:
            sysh.write("\n\t//instance module declaration\n")
        sysh.write('\t%s %s;\n' % (instance_module_name_list[instance_num-1], instance_object_name_list[instance_num-1]))
        line = txt.readline()
    elif 'PortArg' in line:          #提取并存储实例化对象的端口参数
        sign = 'instance'
        var = re.search(': (\w+)', line)
        content = var.group(1)
        names['portarg' + str(instance_num)].append(content)
        line = txt.readline()
    elif 'ParamArg' in line:     #提取实例化参数的内容
        sign = 'paramarg'
        var = re.search(': (\w+)', line)
        content = var.group(1)
        paramarg_list.append(content)
        line = txt.readline()

    elif 'Portlist' in line:
        port_sign = 'exist'
        # sysh.write('SC_MODULE(%s)\n' % module_name)
        # sysh.write('{\n\t//port_list_right declaration\n')
        line = txt.readline()
    elif 'Width' in line:    #端口带位宽[]
        data_type = 1
        line = txt.readline()
    elif 'Input' in line:     #提取input的端口，并存入数组port
        if sentence_sign == 'function':
            portdefine_type = 'uint'
        else:
            portdefine_type = 'input'
        var = re.search(': (\w+)', line)
        content = var.group(1)
        port_content = port_content + content
        port_list_right.append(content)
        line = txt.readline()
    elif 'Inout' in line:     #提取inout的端口，并存入数组port
        portdefine_type = 'inout'
        var = re.search(': (\w+)', line)
        content = var.group(1)
        port_content = port_content + content
        port_list_right.append(content)
        line = txt.readline()
    elif 'Output' in line:     #提取output的端口，并存入数组port
        portdefine_type = 'output'
        var = re.search(': (\w+)', line)
        content = var.group(1)
        port_content = port_content + content
        port_list_right.append(content)
        line = txt.readline()
    elif 'Reg' in line:     #提取Reg的端口，并存入数组port
        var = re.search(': (\w+)', line)
        content = var.group(1)
        if content in port_content:
            port_content = port_content
            content = ''
        else:
            portdefine_type = 'signal'
            port_list_right.append(content)
            port_content = port_content + content
        line = txt.readline()
    elif 'Wire' in line:     #提取Wire的端口，并存入数组port
        var = re.search(': (\w+)', line)
        content = var.group(1)
        if content in port_content:
            pass
        else:
            portdefine_type = 'signal'
            port_list_right.append(content)
            port_content = port_content + content
        line = txt.readline()
    elif 'Integer' in line:     #提取integer的端口，并存入数组port
        portdefine_type = 'integer'
        var = re.search(': (\w+)', line)
        content = var.group(1)
        port_list_right.append(content)
        line = txt.readline()
    elif 'Parameter' in line:     #提取Parameter的端口，并存入数组port
        portdefine_type = 'parameter'
        var = re.search(': (\w+)', line)
        content = var.group(1)
        port_list_right.append(content)
        line = txt.readline()
    elif 'Sens:' in line:    #时序逻辑和组合逻辑
        var = re.search(': (\w+) \(at (\d+)\)', line)
        var1 = var.group(1)
        var2 = var.group(2)
        if var1 == 'all':
            if var2 != '0':
                names['sensalways' + str(always_num)] = []
                names['posedgelist' + str(always_num)] = []
                names['negedgelist' + str(always_num)] = []
                always_type = 2      #组合逻辑内容，给一个标识
                names['sensalways' + str(always_num)].append(var1)
                if always_num == 1:
                    hpp_always_content = hpp_always_content + "\n\t// always blocks\n\tvoid always_combilogic_block%s();\n" % int(always_num)
                else:
                    hpp_always_content = hpp_always_content + "\tvoid always_combilogic_block%s();\n" % int(always_num)
                    # sysc.write(statement_spacenu_num + '}\n}\n')
                line_content = '\nvoid %s::always_combilogic_block%s()\n' % (module_name, int(always_num))
                sysc.write(line_content)
        else:
            # names['posedgelist' + str(always_num)] = []  # 存储上升沿触发信号
            # names['negedgelist' + str(always_num)] = []  # 存储下降沿触发信号
            if var1 == 'posedge':
                always_type = 1  # 时序逻辑内容
                sens_num += 1
                sens_sign = 'pos'
                if sens_num == 1:
                    if always_num == 1:
                        hpp_always_content = hpp_always_content + "\n\t// always blocks\n\tvoid always_block%s();\n" % int(always_num)
                    else:
                        hpp_always_content = hpp_always_content + "\tvoid always_block%s();\n" % int(always_num)
                    line_content = '\nvoid %s::always_block%s()\n' % (module_name, int(always_num))
                    sysc.write(line_content)
                elif sens_num == 2:
                    sysc.write('')
            elif var1 == 'negedge':
                always_type = 1  # 时序逻辑内容
                sens_num += 1
                sens_sign = 'neg'
                if sens_num == 1:
                    if always_num == 1:
                        hpp_always_content = hpp_always_content + "\n\t// always blocks\n\tvoid always_block%s();\n" % int(always_num)
                    else:
                        hpp_always_content = hpp_always_content + "\tvoid always_block%s();\n" % int(always_num)
                    line_content = '\nvoid %s::always_block%s()\n' % (module_name, int(always_num))
                    sysc.write(line_content)
                elif sens_num == 2:
                    sysc.write('')
        line = txt.readline()


    #运算符处理
    elif 'Concat' in line:
        port_num = len(port_list_right)
        bracket_port_num = partselect_num
        brackets_position = port_num-bracket_port_num       #此时列表port下一个数据为括号
        symbol_num += 1
        if symbol_num > 1:
            # bracket_port_num = partselect_num
            port_list_right = brackrts(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right)
        # brackets_symbol = ','
        # brackets_symbol_list.append(brackets_symbol)
        port_num = len(port_list_right)
        brackets_position = port_num  # 此时列表port下一个数据为括号
        partselect_num = 0
        bracket_port_num = 0
        bracket_firstport_num = 0
        line = txt.readline()
    elif 'Partselect' in line:    #端口带有位宽
        data_type = 1
        partselect_num += 1
        if partselect_num > 1 and partselect_num > (partselect_num-1):
            brackets_symbol = ','
            brackets_symbol_list.append(brackets_symbol)
        line = txt.readline()
    elif 'Cond' in line:          #判断符 ？ ：
        data_type = 2
        cond_sign = 'cond'
        line = txt.readline()
        var1 = re.search('(\s+)(\w+):', line)
        cond_block_num = var1.group(1).count(' ')
    elif 'Pointer' in line:       #端口位宽为[]类型
        data_type = 4
        partselect_num += 1
        if partselect_num > 1 and partselect_num > (partselect_num - 1):
            brackets_symbol = ','
            brackets_symbol_list.append(brackets_symbol)
        line = txt.readline()

    #按位操作符（与或非异或）
    elif 'And' in line:       #与&
        var1 = re.search('(\s+)And', line)            #读取And之前的空格，如果与最后一个And空格数相同的identified，既为并列关系
        and_spacenum = var1.group(1).count(' ')
        port_num = len(port_list_right)
        if and_symbol_num == 0:
            if symbol == '':
                symbol = '&'
                symbol_list.append(symbol)
            else:
                if and_spacenum == s_num:
                    symbol = '&'
                    symbol_list.append(symbol)
                else:
                    brackets_symbol = '&'
                    brackets_symbol_list.append(brackets_symbol)
        else:
            if symbol == '&':
                symbol_list.append(symbol)
            elif symbol != '&':
                brackets_symbol = '&'
                brackets_symbol_list.append(brackets_symbol)

        brackets_position = port_num - bracket_port_num
        and_symbol_num += 1
        if and_symbol_num > 1:
            content = brackrts(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right)
        port_num = len(port_list_right)
        brackets_position = port_num
        bracket_port_num, unot_num, bracket_firstport_num = 0, 0, 0
        line = txt.readline()
    elif 'Unot' in line:  #非(~)
        data_type = 3
        unot_num += 1
        var1 = re.search('(\s+)U', line)            #读取unot之前的空格，如果与这个空格数相同的identified，既为并列关系
        unot_spacenum = var1.group(1).count(' ')
        if unot_num == 1:
            unot_space_num = unot_spacenum
        line = txt.readline()
    elif 'Or' in line:   #或|
        if symbol == '' or symbol == '|':
            symbol = '|'
            symbol_list.append(symbol)
        else:
            brackets_symbol = '|'
            brackets_symbol_list.append(brackets_symbol)
        line = txt.readline()
    elif 'Xor' in line:  #异或^
        symbol = '^'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Xnor' in line: #同或~^
        symbol = '~^'
        symbol_list.append(symbol)
        line = txt.readline()

    #逻辑操作符(逻辑或 与 非)
    elif 'Lor' in line:
        if sentence_type == 1:
            brackets_symbol = '||'
            brackets_symbol_list.append(brackets_symbol)
        else:
            symbol = '||'
            symbol_list.append(symbol)
        line = txt.readline()
    elif 'Land' in line:
        if sentence_type == 1:
            brackets_symbol = '&&'
            brackets_symbol_list.append(brackets_symbol)
        elif cond_sign == 'cond':
            brackets_symbol = '&&'
            brackets_symbol_list.append(brackets_symbol)
        else:
            symbol = '&&'
            symbol_list.append(symbol)
        line = txt.readline()
    elif 'Ulnot' in line:   # 非(!)
        # symbol = '!'
        data_type = 5
        var1 = re.search('(\s+)U', line)  # 读取ulnot之前的空格，如果与这个空格数相同的identified，既为并列关系
        unot_space_num = var1.group(1).count(' ')
        line = txt.readline()

    # 算术运算符
    elif 'Plus' in line:
        if data_type == 2:  # ?: 条件选择操作符
            brackets_symbol = '+'
            brackets_symbol_list.append(brackets_symbol)
            port_num = len(port_list_right)
            # brackets_position = bracket_port_num  # 此时列表port下一个数据为括号
            brackets_position = port_num
        else:
            symbol = '+'
            symbol_list.append(symbol)
        plus_identifier_num = 0
        line = txt.readline()
    elif 'Minus' in line:
        symbol = '-'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Times' in line:
        symbol = '*'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Divide' in line:
        symbol = '/'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Mod' in line:
        symbol = '%'
        symbol_list.append(symbol)
        line = txt.readline()

    #关系运算符
    elif 'LessThan' in line:
        symbol = '<'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'LessEq' in line:
        symbol = '<='
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'GreaterThan' in line:
        symbol = '>'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'GreaterEq' in line:
        symbol = '>='
        symbol_list.append(symbol)
        line = txt.readline()

    #等价操作符（!==,===,==）
    elif 'NotEql' in line:
        symbol = '！=='
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Eql' in line:
        symbol = '==='
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Eq' in line:
        symbol = '=='
        symbol_list.append(symbol)
        s_previous_num = 0
        line = txt.readline()

    #移位操作符
    elif 'Srl' in line:
        symbol = '>>'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Sra' in line:
        symbol = '>>>'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Sll' in line:
        symbol = '<<'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Sla' in line:
        symbol = '<<<'
        symbol_list.append(symbol)
        line = txt.readline()

    #归约操作符
    elif 'Uand' in line:
        sign = 'uand'
        symbol = '&'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Unand' in line:
        sign = 'unand'
        symbol = '~&'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Uor' in line:
        sign = 'uor'
        symbol = '|'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Unor' in line:
        sign = 'unor'
        symbol = '~|'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Uxor' in line:
        sign = 'uxor'
        symbol = '^'
        symbol_list.append(symbol)
        line = txt.readline()
    elif 'Uxnor' in line:
        sign = 'uxnor'
        symbol = '~^'
        symbol_list.append(symbol)
        line = txt.readline()

    elif 'FunctionCall' in line:   
        symbol = '()'
        line = txt.readline()

    #特殊关键字，识别就输出上一句
    elif 'Decl' in line:
        var = re.search('at (\d+)', line)
        line_num = int(var.group(1))  # 读取当前的行数
        if line_num != linenum and linenum != 0:  # 行数不同，换行输出上一行内容
            linenum = line_num  # 将当前行数赋给存储行数
            i = 0
            line_content = input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right, line_content)
            if sentence_sign == 'function':
                sysh.write(line_content)
                # function_line_content = line_content
                width = int(port_list_width[0]) - int(port_list_width[1]) + 1  # 计算位宽长度
                sysh.write("\tsc_uint<%s> function_%s" % (width, function_name))
                sysc.write("\nsc_uint<%s> %s::function_%s" % (width, module_name, function_name))
            else:
                hpp_port_content = hpp_port_content + line_content
                sysh_txt.write(line_content)
            port_list_right = []
            port_list_width = []
            port_num, symbol_num, brackets_position, i, bracket_port_num, data_type, bracket_firstport_num, value_type, unot_space_num, value_type = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # 将变量重新初始化
            symbol, brackets_symbol, content, content1, line_content, portdefine_type = '', '', '', '', '', ''
        line = txt.readline()
    elif 'Ioport' in line:
        var = re.search('at (\d+)', line)
        line_num = int(var.group(1))  # 读取当前的行数
        if line_num != linenum and linenum != 0:  # 行数不同，换行输出上一行内容
            linenum = line_num  # 将当前行数赋给存储行数
            i = 0
            line_content = input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right, line_content)
            hpp_port_content = hpp_port_content + line_content
            sysh_txt.write(line_content)
            port_list_right = []
            port_list_width = []
            port_num, symbol_num, brackets_position, i, bracket_port_num, data_type, bracket_firstport_num, value_type, unot_space_num, value_type = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # 将变量重新初始化
            symbol, brackets_symbol, content, content1, line_content = '', '', '', '', ''
        line = txt.readline()
    elif 'Assign' in line:    #assign模块
        var = re.search('at (\d+)',line)
        instance_name = ''
        assign_num += 1
        names['assign' + str(assign_num)] = []
        line_num = int(var.group(1))        #读取当前的行数
        if line_num != linenum and linenum != 0:        #行数不同，换行输出上一行内容
            linenum = line_num      #将当前行数赋给存储行数
            line_content = input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right, line_content)
            if assign_num == 1:
                hpp_port_content = hpp_port_content + line_content
                if sentence_sign == 'always':
                    sysc.write(statement_spacenu_num + '    ' + line_content)
                else:
                    sysh_txt.write(line_content)
                    sysh.write("\n")
                if sentence_sign == 'function':
                    if block_list_level != []:
                        statement_spacenu_num = (block_list_level[-1]) * ' '
                        if case_num != 0:
                            sysc.write(statement_spacenu_num + "    break;\n" + statement_spacenu_num + "}\n")
                        else:
                            sysc.write(statement_spacenu_num + "}\n")
                        del (block_list_level[-1])
                    while block_list_level != []:
                        statement_spacenu_num = block_list_level[-1] * ' '
                        if len(block_list_level) == 1:
                            sysc.write("}\n")
                        else:
                            sysc.write(statement_spacenu_num + "}\n")
                        del (block_list_level[-1])
                    sysc.write(statement_spacenu_num + 'return %s;\n}\n' % function_name)
                else:
                    while block_list_level != []:
                        statement_spacenu_num = block_list_level[-1] * ' '
                        if len(block_list_level) == 1:
                            sysc.write("}\n")
                        else:
                            sysc.write(statement_spacenu_num + "}\n")
                        del (block_list_level[-1])

            else:
                if symbol == '()':
                    sysc.write("}\n")
                else:
                    sysc.write(line_content)  # 输出上一行内容
                    while block_list_level != []:
                        statement_spacenu_num = block_list_level[-1] * ' '
                        if len(block_list_level) == 1:
                            sysc.write("}\n")
                        else:
                            sysc.write(statement_spacenu_num + "}\n")
                        del (block_list_level[-1])
            sentence_sign = 'assign'
            port_list_right = []
            symbol_list = []
            brackets_symbol_list = []
            port_num, symbol_num, brackets_position, i, bracket_port_num, data_type, bracket_firstport_num, value_type, unot_space_num, value_type = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0     #将变量重新初始化
            portdefine_type, sentence_type = 0, 0
            partselect_num, and_symbol_num = 0, 0
            nonblockingsubstitution_num = 0
            symbol, brackets_symbol, content, content1, sign, s_num = '', '', '', '', '', ''
            lvalue_selection_port, port_left = '', ''
        # if sentence_sign == 'function':
        #     if block_list_level != []:
        #         statement_spacenu_num = (block_list_level[-1]) * ' '
        #         if case_num != 0:
        #             sysc.write(statement_spacenu_num + "    break;\n" + statement_spacenu_num + "}\n")
        #         else:
        #             sysc.write(statement_spacenu_num + "}\n")
        #         del (block_list_level[-1])
        #     while block_list_level != []:
        #         statement_spacenu_num = block_list_level[-1] * ' '
        #         if len(block_list_level) == 1:
        #             sysc.write("}\n")
        #         else:
        #             sysc.write(statement_spacenu_num + "}\n")
        #         del (block_list_level[-1])
        #     while block_list_level != []:
        #         sysc.write('    ' + statement_spacenu_num + "break;\n")
        #         sysc.write(statement_spacenu_num + "}\n")
        #         space_num = space_num - 4
        #         statement_spacenu_num = space_num * ' '
        #         del (block_list_level[-1])
        #     sysc.write(statement_spacenu_num + "}\n")
        #     sysc.write(statement_spacenu_num + 'return %s;\n}\n' % function_name)
        #     sentence_sign = ''

        line_content = '\nvoid %s::assign_' % module_name        #assign部分转换内容
        if assign_num == 1:
            hpp_assign_content1 = '\n\t// assign blocks\n\tvoid assign_'
            hpp_assign_content = hpp_assign_content + hpp_assign_content1
        else:
            hpp_assign_content1 = "\tvoid assign_"
            hpp_assign_content = hpp_assign_content + hpp_assign_content1
        portdefine_type = 0
        casestatement = ''
        lvalue_selection_port, port_left = '', ''
        else_sign = ''
        intconst_num = ''
        sentence_sign = 'assign'
        line = txt.readline()
    elif 'Always' in line:   #always模块
        block_current_num, ifstatement_num, sens_num = 0, 0, 0
        instance_name = ''
        ifstatement_list_if = []
        always_num += 1
        sentence_sign = 'always'
        names['always' + str(always_num)] = []
        var = re.search('at (\d+)', line)
        line_num = int(var.group(1))        #读取当前的行数
        if line_num != linenum and linenum != 0:        #行数不同，换行输出上一行内容
            linenum = line_num      #将当前行数赋给存储行数
            line_content = input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right, line_content)
            if portdefine_type == 'signal':
                hpp_port_content = hpp_port_content + line_content
                sysh_txt.write(line_content)
            else:
                if line_content != "":
                    sysc.write("    " + statement_spacenu_num + line_content)  # 输出上一行内容
                if block_list_level != []:
                    statement_spacenu_num = (block_list_level[-1]) * ' '
                    if case_num != 0:
                        sysc.write(statement_spacenu_num + "    break;\n" + statement_spacenu_num + "}\n")
                        del (block_list_level[-1])
                    # else:
                    #     sysc.write(statement_spacenu_num + "}22222\n")
                    # del (block_list_level[-1])
                while block_list_level != []:
                    statement_spacenu_num = block_list_level[-1] * ' '
                    if len(block_list_level) == 1:
                        sysc.write("}\n")
                    else:
                        sysc.write(statement_spacenu_num + "}\n")
                    del (block_list_level[-1])
            port_list_right = []   #数组、变量清零
            block_list_level = []
            block_list_case = []
            brackets_symbol_list = []
            symbol_list = []
            port_num, symbol_num, brackets_position, i, bracket_port_num, data_type, bracket_firstport_num, unot_space_num, value_type = 0, 0, 0, 0, 0, 0, 0, 0, 0
            block_space_num, block_current_num, portdefine_type, space_num = 0, 0, 0, 0
            partselect_num, and_symbol_num = 0, 0
            case_num = 0
            nonblockingsubstitution_num = 0
            symbol, brackets_symbol, content, content1, line_content = '', '', '', '', ''
            casestatement = ''
            lvalue_selection_port = ''
            else_sign = ''
            port_left_type = ''
            port_right_type = ''
        line = txt.readline()

    elif 'Function:' in line:   #function模块
        if case_num != 0:   #输出case语句的最后一个部分
            sysc.write('    ' + statement_spacenu_num + "break;\n")
            while block_list_level != []:
                statement_spacenu_num = block_list_level[-1] * ' '
                sysc.write(statement_spacenu_num + "}\n")
                del (block_list_level[-1])
            sysc.write("}\n")

        block_current_num, space_num, case_num, ifstatement_num = 0, 0, 0, 0
        ifstatement_list_if = []
        block = ''
        casestatement = ''
        var = re.search('at (\d+)', line)
        line_num = int(var.group(1))  # 读取当前的行数
        var1 = re.search(': (\w+)', line)      #提取function的函数名，并存储起来
        function_name = '%s' % var1.group(1)

        if line_num != linenum and linenum != 0:        #行数不同，换行输出上一行内容
            linenum = line_num      #将当前行数赋给存储行数
            line_content = input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right, line_content)
            if portdefine_type == 'input' or portdefine_type == 'inout' or portdefine_type == 'output' or portdefine_type == 'signal' or portdefine_type == 'integer':
                sysh.write(line_content)        #如果function模块前是端口和信号就输出上一行内容
            elif sentence_sign == 'assign':
                sysc.write(line_content)  # 如果function模块前是assign就输出上一行内容
            port_list_right = []  # 数组、变量清零
            port_list_width = []
            brackets_symbol_list = []
            port_list_right.append(var1.group(1))
            block_list_level = []
            port_num, symbol_num, brackets_position, i, bracket_port_num, data_type, bracket_firstport_num, unot_space_num, value_type = 0, 0, 0, 0, 0, 0, 0, 0, 0
            block_space_num, block_current_num = 0, 0
            symbol, brackets_symbol, content, content1, line_content = '', '', '', '', ''
        portdefine_type = 'signal'
        sentence_sign = 'function'
        line = txt.readline()
    elif 'ForStatement' in line:
        sign = 'for'
        sysc.write("\n\tfor(")
        line = txt.readline()

    elif 'Lvalue' in line:      #判断Identifier读取为等号左边端口
        value_type = 1
        ifelse_sign = 0
        line = txt.readline()
    elif 'Rvalue' in line:      #判断Identifier读取为等号右端口
        value_type = 2
        ifelse_sign = 0
        partselect_num = 0
        line = txt.readline()

    #标识符和整数常量处理
    elif 'Identifier' in line:
        var = re.search(': (\w+) ', line)      #匹配Identifier的内容
        var1 = re.search('(\s+)Iden', line)     #匹配Identifier前的空格数
        if value_type == 1:             #等号左边端口
            if sentence_type == 2:    #过程赋值语句（在always内或function内）
                if data_type == 1:         #带位宽类型
                    content1 = '%s' % var.group(1)
                    if content1 in port_left:   #判断该信号是否已经出现过
                        content1 = lvalue_selection_port
                    else:
                        port_left = '%s' % content1
                        content1 = 'var_%s' % content1
                        lvalue_selection_port = content1
                        sysc.write('    ' + statement_spacenu_num + '%s = %s.read();\n' % (lvalue_selection_port, port_left))
                        sysh_txt.close()
                        sysh_txt = open('test/%s_txt.txt' % input_file, 'r+')
                        syshline = sysh_txt.readline()
                        while syshline:    #查找该变量对应的数据类型和位宽大小
                            if port_left in syshline:
                                var2 = re.search('<(sc_(\w+)<\d+>) > %s' % port_left, syshline)
                                content = '\t%s %s;\n' % (var2.group(1), lvalue_selection_port)
                                port_left_type = '%s' % var2.group(2)
                                if content in hpp_port_content:
                                    pass
                                else:
                                    hpp_port_content = hpp_port_content + content
                            syshline = sysh_txt.readline()
                else:            #其他类型
                    content1 = var.group(1)
                    if sentence_sign == 'always':  #该语句是always语句
                        names['always' + str(always_num)].append(content1)
                        content = '%s = ' % (content1)
                        if lvalue_selection_port != '':
                            sysc.write('    ' + statement_spacenu_num + '%s = %s;\n' % (port_left, lvalue_selection_port))
                            lvalue_selection_port = ''
                        sysh_txt.close()
                        sysh_txt = open('test/%s_txt.txt' % input_file, 'r+')
                        syshline = sysh_txt.readline()
                        while syshline:
                            if var.group(1) in syshline:
                                var2 = re.search('(\w+<\d+|bool)> (.*)%s' % content1, syshline)
                                if 'sc_' in var2.group(1):
                                    var3 = re.search('sc_(\w+)', var2.group(1))
                                    port_left_type = '%s' % var3.group(1)
                                else:
                                    port_left_type = '%s' % var2.group(1)
                            syshline = sysh_txt.readline()
                    elif sentence_sign == 'function':  #该语句是function语句
                        content = '%s = ' % content1
                    else:   #其他语句情况
                        content = '%s = ' % content1
                    line_content = content
                    content = ''
            else:   #其他类型语句
                if data_type == 1:         #带位宽类型
                    content1 = '%s' % var.group(1)
                    names['assign' + str(assign_num)].append(content1)
                    if content1 in port_left:
                        content1 = lvalue_selection_port
                    else:
                        port_left = '%s' % content1
                        content1 = 'var_%s' % content1
                        lvalue_selection_port = content1
                        sysh_txt.close()
                        sysh_txt = open('test/%s_txt.txt' % input_file, 'r+')
                        syshline = sysh_txt.readline()
                        while syshline:
                            if port_left in syshline:
                                var2 = re.search('<(sc_(\w+)<\d+>) > (.*)%s' % port_left, syshline)
                                content = '\t%s %s;\n' % (var2.group(1), lvalue_selection_port)
                                port_left_type = '%s' % var2.group(2)
                                if content in hpp_port_content:
                                    pass
                                else:
                                    hpp_port_content = hpp_port_content + content
                            syshline = sysh_txt.readline()
                        content = "%s()\n{\n\t" % port_left  # 左端端口应输出值
                        hpp_assign_content = hpp_assign_content + "%s();\n" % names['assign' + str(assign_num)][0]
                        line_content = line_content + content
                        content = ''
                else:
                    content1 = var.group(1)
                    port_left = '%s' % content1
                    names['assign' + str(assign_num)].append(content1)
                    hpp_assign_content = hpp_assign_content + "%s();\n" % names['assign' + str(assign_num)][0]
                    sysh_txt.close()
                    sysh_txt = open('test/%s_txt.txt' % input_file, 'r+')
                    syshline = sysh_txt.readline()
                    while syshline:
                        if var.group(1) in syshline:
                            var2 = re.search('<(\w+<\d+|bool)> (.*)%s' % content1, syshline)
                            if 'sc_' in var2.group(1):
                                var3 = re.search('sc_(\w+)', var2.group(1))
                                port_left_type = '%s' % var3.group(1)
                            else:
                                port_left_type = '%s' % var2.group(1)
                        syshline = sysh_txt.readline()
                    content = "%s()\n{\n\t%s = " % (var.group(1), var.group(1))  # 左端端口应输出值
                    line_content = line_content + content
                    content = ''
        elif value_type == 2:       #等号右边端口
            s_num = var1.group(1).count(' ')           #identifier前面的空格数
            and_space_num = and_spacenum
            content1 = var.group(1)
            if data_type == 1 or data_type == 4:       #语句是带位宽类型或端口尾款为[]形式
                if sentence_sign == 'assign':
                    names['assign' + str(assign_num)].append(content1)
                sysh_txt.close()
                sysh_txt = open('test/%s_txt.txt' % input_file, 'r+')
                syshline = sysh_txt.readline()
                while syshline:
                    if content1 in syshline:
                        var2 = re.search('(\w+<\d+|bool)> (.*)%s' % content1, syshline)
                        if 'sc_' in var2.group(1):
                            var3 = re.search('sc_(\w+)', var2.group(1))
                            port_right_type = '%s' % var3.group(1)
                        else:
                            port_right_type = '%s' % var2.group(1)
                    syshline = sysh_txt.readline()
                content2 = 'var_%s' % content1
                if content2 == lvalue_selection_port:
                    content1 = lvalue_selection_port
            elif data_type == 2:      #语句是判断类型(即（）？：)
                # 如果当前变量前空格数与上一个数（二进制数/其他数）前的空格数相同，表明两部分属于同一块
                if s_num == intconst_num and bracket_port_num == 1:
                    bracket_port_num = 0
                if bracket_port_num == 0:  #bracket_port_num用于判断该变量或语句属于条件选择语句的哪个部分，0表示判断条件部分，1表示判断条件为真时运算结果，2表示判断条件为假时运算结果
                    if symbol == '<':
                        content = '(%s.read()' % content1
                    else:
                        content = '%s.read()' % content1
                        if symbol == '':
                            port_list_right.append(content)
                    if sentence_sign == 'assign':
                        names['assign' + str(assign_num)].append(content1)
                    if s_num == cond_block_num:
                        bracket_port_num = 1
                else:
                    if bracket_port_num == 1:  #判断条件为真的运算结果处理
                        if brackets_symbol != '':
                            content = '%s.read()' % content1
                            if brackets_symbol == '+' and data_type != 5:
                                plus_identifier_num = s_num
                        else:
                            content = '? %s :' % content1
                            bracket_port_num = 2
                        if sentence_sign == 'assign':
                            names['assign' + str(assign_num)].append(content1)
                        # bracket_port_num = 2
                    else:  #判断条件为假的运算结果处理
                        content = '%s' % content1
                        if sentence_sign == 'assign':
                            names['assign' + str(assign_num)].append(content1)
                        bracket_port_num = 0
                        symbol = ''
                    port_list_right.append(content)
                    content = ''
            elif data_type == 3:      #语句括号中端口含有非~
                if bracket_port_num == 0:
                    if sentence_sign == 'assign':
                        names['assign' + str(assign_num)].append(content1)
                    content = '~%s.read()' % content1
                    if sentence_type == 2 and symbol == '':  # 过程赋值语句，并且语句内没有特殊符号
                        line_content = line_content + content + ';\n'
                        sysc.write(statement_spacenu_num + line_content)
                        # sysc.write('    ' + statement_spacenu_num + line_content)
                        line_content, content = '', ''
                        port_list_right = []
                else:
                    if s_num == bracket_firstport_num:  #identifier读取到的信号与第一个信号是同层
                        content1 = '%s' % content1
                        names['assign' + str(assign_num)].append(content1)
                        content = '~%s.read()' % content1
                    elif s_num == unot_space_num:    #用于存储~unot之前的空格数，判断identifier读取到的端口是否为并列关系
                        if unot_spacenum != unot_space_num:   #identifier读取到的信号
                            content = '~%s.read()' % content1
                        else:
                            content = '%s.read()' % content1
                    else:
                        content = '~%s.read()' % content1
                        names['assign' + str(assign_num)].append(content1)
                data_type = 0
                port_list_right.append(content)
            elif data_type == 5:    #语句括号中端口含有非 !
                content = '!%s.read()' % content1
                port_list_right.append(content)
            elif symbol == '()':  #函数语句类型
                func_identifier_num += 1
                if func_identifier_num == 1:    #函数语句里的第一个信号为函数名
                    function_name = content1
                else:
                    content = 'function_%s(%s);\n' % (function_name, content1)
                    line_content = '    ' + statement_spacenu_num + line_content + content
                    sysc.write(line_content)
                    func_identifier_num = 0
                if sentence_sign == 'assign':
                    names['assign' + str(assign_num)].append(content1)
                elif sentence_sign == 'always':
                    names['always' + str(always_num)].append(content1)
            elif symbol == '+':
                if sign == 'for':   #for循环语句
                    content = '%s +' % content1
                    line_content = line_content + content
                else:  #其他含有'+'的语句
                    content = '%s.read()' % content1
                    port_list_right.append(content)
                    # line_content = line_content + content
                if sentence_sign == 'always':
                    names['always' + str(always_num)].append(content1)
                elif sentence_sign == 'assign':
                    names['assign' + str(assign_num)].append(content1)
            else:
                if sentence_type == 2:    #过程赋值语句
                    names['always' + str(always_num)].append(content1)
                    if sign == 'for':
                        content = '%s' % content1
                    else:
                        content = '%s.read()' % content1
                else:
                    names['assign' + str(assign_num)].append(content1)
                    content = '%s.read()' % content1
                if sentence_type == 2 and symbol == '':   #过程赋值语句，并且语句内没有特殊符号
                    line_content = line_content + content + ';\n'
                    sysc.write('    ' + statement_spacenu_num + line_content)
                    line_content = ''
                else:#如果是for就不放入队列*****
                    if sign == 'for':
                        content = content
                    else:
                        port_list_right.append(content)
            if brackets_symbol != '':
                if bracket_port_num == 0:
                    if s_num == cond_block_num or bracket_firstport_num == 0:
                        bracket_port_num = 1
                    bracket_firstport_num = s_num  # 括号第一个端口identifier之前的空格数
                else:
                    if s_num == bracket_firstport_num or s_num == unot_space_num or s_num == and_space_num:         #空格数相同，是同一个括号里的内容，括号里端口统计加一
                        bracket_port_num += 1
                    elif plus_identifier_num == unot_space_num and plus_identifier_num != 0 and unot_space_num != 0:
                        bracket_port_num += 1
                    elif s_num > bracket_firstport_num and bracket_firstport_num != 0:
                        bracket_port_num += 1
                    elif s_num == plus_identifier_num:
                        bracket_port_num += 1
                    else:                       #空格数不同，不是括号里的内容，统计不变
                        bracket_port_num = bracket_port_num
        elif value_type == 0:      #端口为无等式端口
            s_num = var1.group(1).count(' ')
            content1 = var.group(1)
            if data_type == 5:    #语句内非号为!形式
                if bracket_port_num == 0:
                    content = '!%s.read()' % content1
                    bracket_firstport_num = s_num  # 括号第一个端口identifier之前的空格数
                    bracket_port_num = 1
                else:
                    if s_num == bracket_firstport_num:
                        content = '!%s.read()' % content1
                    elif s_num == unot_space_num:  # 空格数相同，是同一个括号里的内容，括号里端口统计加一
                        content = '%s.read()' % content1
                    else:  # 空格数不同，不是括号里的内容，统计不变
                        bracket_port_num = bracket_port_num
                port_list_right.append(content)
                data_type = 0
            elif data_type == 3:   #语句内非号为~形式
                content = '~%s.read()' % content1
                port_list_right.append(content)
                data_type = 0
            elif symbol == '==':    #语句含有==
                if s_num == s_previous_num:   #当前信号identifier前的空格与上一个相同
                    content = '%s.read() == %s ' % (content, content1)
                    port_list_right.append(content)
                else:
                    content = content1
            elif symbol == '<':
                content = content1
            elif symbol == '<=':
                content = content1
            elif symbol == '>':
                content = content1
            elif symbol == '>=':
                content = content1
            elif symbol == '!==':    #语句含有!==
                content = content1
            elif symbol == '===':    #语句含有===
                content = content1
            elif always_type == 1 or always_type == 2:    #语句含有敏感信号
                content = content1
                if sens_num == 1:
                    names['sensalways' + str(always_num)] = []   # 存储组合逻辑的所有信号
                    names['posedgelist' + str(always_num)] = []  # 存储上升沿触发信号
                    names['negedgelist' + str(always_num)] = []  # 存储下降沿触发信号
                if sens_sign == 'pos':
                    names['posedgelist' + str(always_num)].append(content)
                elif sens_sign == 'neg':
                    names['negedgelist' + str(always_num)].append(content)
                else:
                    names['always' + str(always_num)].append(content)
                if sentence_type == 4:   #switch语句
                    statement_spacenu_num = block_list_level[-1] * ' '
                    if sentence_sign == 'function':
                        sysc.write(statement_spacenu_num + 'switch(func_%s)\n' % content1)
                    else:
                        sysc.write(statement_spacenu_num + 'switch(%s.read())\n' % content1)
                    sysc.write(statement_spacenu_num + '{\n')
                    sentence_type = 0
            elif sentence_type == 3:   #case语句
                # statement_spacenu_num = space_num * ' '
                #statement_spacenu_num = block_list_level[-1] * ' '
                if case_num == 1:
                    statement_spacenu_num = block_list_level[-1] * ' '
                else:
                    statement_spacenu_num = block_list_level[-1] * ' '
                sysc.write(statement_spacenu_num + 'case %s:\n' % content1)
                sentence_type = 0
            elif sign == 'instance':  #实例化语句
                content = content1
                names['instance' + str(instance_num)].append(content)
                sign = ''
            elif sentence_type == 4:   #switch语句
                if block_list_level != []:
                    statement_spacenu_num = block_list_level[-1] * ' '
                if sentence_sign == 'function':
                    sysc.write('\n' + statement_spacenu_num + 'switch(func_%s)\n' % content1)
                else:
                    sysc.write(statement_spacenu_num + 'switch(%s.read())\n' % content1)
                sysc.write(statement_spacenu_num + '{\n')
                sentence_type = 0
            else:
                content = '%s.read()' % content1
                port_list_right.append(content)
            if brackets_symbol != '':
                if bracket_port_num == 0:
                    bracket_firstport_num = s_num              #括号第一个端口identifier之前的空格数
                    bracket_port_num = 1
                else:
                    if s_num == bracket_firstport_num or s_num == unot_space_num:         #空格数相同，是同一个括号里的内容，括号里端口统计加一
                        bracket_port_num += 1
                    else:                       #空格数不同，不是括号里的内容，统计不变
                        bracket_port_num = bracket_port_num
            s_previous_num = s_num    #将当前空格数存起来，与下一个进行比较
        line = txt.readline()
    elif 'IntConst' in line:
        if portdefine_type == 'input' or portdefine_type == 'inout' or portdefine_type == 'output' or portdefine_type == 'signal' or portdefine_type == 'uint' or portdefine_type == 'integer':
            var = re.search(': (\d+) ', line)
            content = var.group(1)
            port_list_width.append(content)
        elif portdefine_type == 'parameter':    #参数类型
            var = re.search('\d*\'(b|d|o|h)(\w+)', line)
            var1 = var.group(1)
            if var1 == 'b':
                content1 = '0b%s' % var.group(2)
            elif var1 == 'd':
                content1 = '%s' % var.group(2)
            elif var1 == 'o':
                content1 = '0%s' % var.group(2)
            elif var1 == 'h':
                content1 = '0x%s' % var.group(2)
            else:
                content1 = '%s' % var.group(2)

            if port_sign == '':
                content = '\tint %s_%s = ' % (module_name, port_list_right[i])
            else:
                content = '\tsc_uint<%s> %s = ' % (len(var.group(2)),port_list_right[i])
            line_content = content + content1
            sysh.write('%s;\n' % line_content)
            line_content, content, var, var1, content1 = '', '', '', '', ''
        elif sign == 'paramarg':    #实例化类型
            var = re.search('\d*\'(b|d|o|h)(\w+)', line)
            var1 = var.group(1)
            if var1 == 'b':
                content1 = '0b%s' % var.group(2)
            elif var1 == 'd':
                content1 = '%s' % var.group(2)
            elif var1 == 'o':
                content1 = '%s' % var.group(2)
            elif var1 == 'h':
                content1 = '0x%s' % var.group(2)
            if len(paramarg_list) == 2:
                content = '%s_%s_%s = %s;' % (instance_object_name_list[instance_num-1], instance_module_name_list[instance_num-1], content, content1)
                paramarg_content_list.append(content)
            else:
                content = ''
        elif data_type == 1:     #带位宽类型
            i += 1              #统计读取到inconst次数，第一次输出range(%d,第二次输出%d)
            var = re.search(': (\d+) ', line)
            # if content in port_content:
            #     pass
            if i == 1:  #高位宽情况
                # if sentence_sign == 'assign' or sentence_sign == 'always'
                if sentence_type == 2:    #过程赋值语句
                    if port_left_type != port_right_type:    #等号左边信号类型和右边信号类型不同
                        if port_right_type != '':
                            if content2 == lvalue_selection_port:
                                content = '.range(%s,' % var.group(1)
                            else:
                                content = '.read().range(%s,' % var.group(1)
                        else:
                            content = '.range(%s,' % var.group(1)
                    else:   #等号左边信号类型和右边信号类型相同
                        if value_type == 2:   #等号右边信号
                            if content2 == lvalue_selection_port:
                                content = '.range(%s,' % var.group(1)
                            else:
                                content = '.read().range(%s,' % var.group(1)
                        else:        #等号左边信号
                            content = '.range(%s,' % var.group(1)
                else:  # assign语句
                    if value_type == 1:   #等号左边信号
                        content = '.range(%s,' % var.group(1)
                    else:    #等号右边信号
                        if content == '':
                            if sentence_sign == 'assign':
                                content = '.read().range(%s,' % var.group(1)
                            else:
                                pass
                        else:
                            content = '.read().range(%s,' % var.group(1)
                content = content1 + content     #将端口与位宽连接起来
            else:  #低位宽情况
                if sentence_type == 2 and value_type == 1:    #赋值语句的左值
                    content1 = '%s) = ' % var.group(1)
                elif sentence_sign == 'assign':
                    if value_type == 1:   #assign语句左值
                        content1 = '%s) =' % var.group(1)
                    else:    #assign语句右值
                        content1 = '%s)' % var.group(1)
                else:
                    if port_left_type != port_right_type:
                        if port_right_type != '' and port_left_type != '':
                            content1 = '%s).to_%s()' % (var.group(1), port_left_type)
                        else:
                            content1 = '%s)' % var.group(1)
                    else:
                        if content == '':
                            if sentence_sign == 'assign':
                                content1 = '%s)' % var.group(1)
                            else:
                                pass
                        else:
                            content1 = '%s)' % var.group(1)
                content = content + content1
                # bracket_port_num += 1
                i, data_type = 0, 0              #变量清0
                if sentence_type == 2 and value_type == 1:  #过程赋值语句的左值
                    line_content = content
                elif sentence_type == 2 and value_type == 2:  #过程赋值语句的右值
                    if symbol != '':    #语句中有符号
                        port_list_right.append(content)
                    else:   #语句中无符号
                        line_content = line_content + content
                        sysc.write('    ' + statement_spacenu_num+'%s;\n' % line_content)
                        line_content = ''
                else:  #其他情况
                    if lvalue_selection_port != '':    #左值信号的中间变量不为空
                        content2 = "%s = %s;\n\t" % (lvalue_selection_port, port_left)
                        if content2 in port_list_right:
                            pass
                        else:
                            port_list_right.append(content2)
                    if content == '':
                        pass
                    else:
                        port_list_right.append(content)
                    content = ''
                    if portdefine_type == "integer":    #信号类型是整数
                        del(port_list_right[-1])
                    else: #其他情况
                        port_num = len(port_list_right)
        elif data_type == 2:     #语句是条件选择语句类型(即（）？：)
            var = re.search('\d*\'(\w)(\w+)', line)
            var2 = re.search('(\s+)IntConst:', line)
            intconst_num = var2.group(1).count(' ')           #提取记录intconst前面的空格数，用于判断该部分是条件选择语句中的哪个部分
            if intconst_num == cond_block_num:   #intconst前的空格数与cond下一行内容的空格数相同，表示两者是同层关系
                if bracket_port_num == 0:
                    bracket_port_num = 1
                # 进行进制(二、八、十、十六进制)的判断
                var1 = var.group(1)
                if var1 == 'b':
                    content1 = '0b%s' % var.group(2)
                elif var1 == 'd':
                    content1 = '%s' % var.group(2)
                elif var1 == 'o':
                    content1 = '0%s' % var.group(2)
                elif var1 == 'h':
                    content1 = '0x%s' % var.group(2)
                # 进行位宽的添加
                sysh_txt.close()
                sysh_txt = open('test/%s_txt.txt' % input_file, 'r+')
                syshline = sysh_txt.read()
                if port_left in syshline:
                    var1 = re.search('(sc_\w+<\d+>)', syshline)
                    content2 = '(%s)' % var1.group(1)
                # 进制、位宽、数字的组合
                if bracket_port_num == 1:
                    content = '? %s %s : ' % (content2, content1)
                    bracket_port_num = 2
                elif bracket_port_num == 2:
                    content = '%s %s' % (content2, content1)
                    symbol = ''
                    # bracket_port_num = 0
            else:   #intconst前的空格数与cond下一行内容的空格数不同，该部分为条件选择语句三大部分其中一块的一小部分
                if symbol == '<':
                    content1 = ' < %s)' % var.group(2)
                    content = content + content1
                # elif symbol == '>':
                #     content1 = ' > %s)' % var.group(2)
                #     content = content + content1
                # elif symbol == '==':
                #     content1 = ' == %s)' % var.group(2)
                #     content = content + content1
                else:
                    # 进行进制(二、八、十、十六进制)的判断
                    var1 = var.group(1)
                    if var1 == 'b':
                        content1 = '0b%s' % var.group(2)
                    elif var1 == 'd':
                        content1 = '%s' % var.group(2)
                    elif var1 == 'o':
                        content1 = '0%s' % var.group(2)
                    elif var1 == 'h':
                        content1 = '0x%s' % var.group(2)
                    else:
                        content1 = '%s' % var.group(2)
                    content = '%s %s %s' % (content, symbol, content1)
            symbol = ''
            if '<' in symbol_list:
                bracket_port_num = 1
            port_list_right.append(content)
        elif data_type == 4:    #语句端口尾是[]形式
            var = re.search(': (\d+) ', line)
            content = '.read()[%s]' % var.group(1)
            content = content1 + content
            port_list_right.append(content)
        elif symbol == '+':
            var = re.search(': \d*\'*(b|d|o|h)*(\w+)', line)
            # 进行进制(二、八、十、十六进制)的判断
            var1 = var.group(1)
            if var1 == 'b':
                content1 = '0b%s' % var.group(2)
            elif var1 == 'd':
                content1 = '%s' % var.group(2)
            elif var1 == 'o':
                content1 = '0%s' % var.group(2)
            elif var1 == 'h':
                content1 = '0x%s' % var.group(2)
            else:
                content1 = '%s' % var.group(2)
            if sign == 'for':
                content2 = ' %s)' % content1
                content = line_content + content2
                port_list_right.append(content)
                symbol, line_content = '', ''
            else:
                content2 = '%s' % content1
                port_list_right.append(content2)

        elif symbol == '==':    #语句含有==
            var = re.search(': \d*\'*(b|d|o|h)*(\w+)', line)
            # 进行进制(二、八、十、十六进制)的判断
            var1 = var.group(1)
            if var1 == 'b':
                content1 = '0b%s' % var.group(2)
            elif var1 == 'd':
                content1 = '%s' % var.group(2)
            elif var1 == 'o':
                content1 = '0%s' % var.group(2)
            elif var1 == 'h':
                content1 = '0x%s' % var.group(2)
            else:
                content1 = '%s' % var.group(2)
            content2 = '.read() == %s' % content1
            content = content + content2
            port_list_right.append(content)
        elif symbol == '>>':   #语句含有>>
            var = re.search('(\w+) ', line)
            content1 = '>> %s' % var.group(1)
            port_list_right.append(content1)
            symbol = ''
        elif symbol == '>>>':   #语句含有>>>
            var = re.search('(\w+) ', line)
            content1 = ' >>> %s' % var.group(1)
            port_list_right.append(content1)
            symbol = ''
        elif symbol == '<<':   #语句含有<<
            var = re.search('(\w+) ', line)
            content1 = ' << %s' % var.group(1)
            port_list_right.append(content1)
            symbol = ''
        elif symbol == '<<<':   #语句含有<<<
            var = re.search('(\w+) ', line)
            content1 = ' <<< %s' % var.group(1)
            port_list_right.append(content1)
            symbol = ''
        elif symbol == '<':   #语句含有<
            var = re.search(': \d*\'*(b|d|o|h)*(\w+)', line)
            # 进行进制(二、八、十、十六进制)的判断
            var1 = var.group(1)
            if var1 == 'b':
                content1 = '0b%s' % var.group(2)
            elif var1 == 'd':
                content1 = '%s' % var.group(2)
            elif var1 == 'o':
                content1 = '0%s' % var.group(2)
            elif var1 == 'h':
                content1 = '0x%s' % var.group(2)
            else:
                content1 = '%s' % var.group(2)
            if sign == 'for':
                content2 = ' < %s;' % content1
            else:
                content2 = '.read() < %s' % content1
            # content1 = '.read() < 0%s' % var.group(1)
            content = content + content2
            port_list_right.append(content)
            symbol = ''
        elif symbol == '<=':
            var = re.search('(\w+) ', line)
            content1 = ' <= %s' % var.group(1)
            content = content + content1
            port_list_right.append(content)
        elif symbol == '>':   #语句含有>
            var = re.search(': \d*\'*(b|d|o|h)*(\w+)', line)
            # 进行进制(二、八、十、十六进制)的判断
            var1 = var.group(1)
            if var1 == 'b':
                content1 = '0b%s' % var.group(2)
            elif var1 == 'd':
                content1 = '%s' % var.group(2)
            elif var1 == 'o':
                content1 = '0%s' % var.group(2)
            elif var1 == 'h':
                content1 = '0x%s' % var.group(2)
            else:
                content1 = '%s' % var.group(2)
            # var = re.search('\'(\w+) ', line)
            # content1 = '.read() > 0%s' % var.group(1)
            content = content + content1
            port_list_right.append(content)
            symbol = ''
        elif symbol == '>=':
            var = re.search('(\w+) ', line)
            content1 = ' >= %s' % var.group(1)
            content = content + content1
            port_list_right.append(content)
        elif symbol == '!==':    #语句含有!==
            var = re.search('\'(\w+) ', line)
            content1 = '.read() !== 0%s' % var.group(1)
            content = content + content1
            port_list_right.append(content)
        elif symbol == '===':    #语句含有===
            var = re.search('\'(\w+) ', line)
            content1 = '.read() === 0%s' % var.group(1)
            content = content + content1
            port_list_right.append(content)
        elif sentence_type == 2:    #过程赋值语句
            var = re.search(': \d*\'*(b|d|o|h)*(\w+)', line)
            # 进行进制(二、八、十、十六进制)的判断
            var1 = var.group(1)
            if var1 == 'b':
                content = '0b%s' % var.group(2)
            elif var1 == 'd':
                content = '%s' % var.group(2)
            elif var1 == 'o':
                content = '0%s' % var.group(2)
            elif var1 == 'h':
                content = '0x%s' % var.group(2)
            else:
                content = '%s' % var.group(2)
            # var2 = re.search(': (\S+)', line)
            # content2 = var2.group(1)
            # if 'b' in content2 or 'd' in content2 or 'o' in content2 or 'h' in content2:
            #     var = re.search('\d*\'(b|d|o|h)(\w+)', line)
            #     var1 = var.group(1)
            #     if var1 == 'b':
            #         content = '0b%s' % var.group(2)
            #     elif var1 == 'd':
            #         content = '%s' % var.group(2)
            #     elif var1 == 'o':
            #         content = '%s' % var.group(2)
            #     elif var1 == 'h':
            #         content = '0x%s' % var.group(2)
            # else:
            #     var = re.search(': (\d+)', line)
            #     content = '%s' % var.group(1)
            line_content = line_content + content
            if sign == 'for':
                port_list_right.append(line_content + ';')
            else:
                sysc.write('    ' + statement_spacenu_num + '%s;\n' % line_content)
            line_content, content, var, var1, content1, content2 = '', '', '', '', '', ''
            data_type = 0
        elif sentence_type == 3:     #case语句
            var = re.search('\d*\'(b|d|o|h)(\w+)', line)
            var1 = var.group(1)
            case_intconst = 'yes'
            if var1 == 'b':
                content = '0b%s' % var.group(2)
            elif var1 == 'd':
                content = '%s' % var.group(2)
            elif var1 == 'o':
                content = '%s' % var.group(2)
            elif var1 == 'h':
                content = '0x%s' % var.group(2)
            if case_num == 1:
                sysc.write('    ' + statement_spacenu_num + 'case %s:\n' % content)
            else:
                sysc.write(statement_spacenu_num + 'case %s:\n' % content)

        line = txt.readline()
    elif 'StringConst' in line:
        var = re.search(': (\w+)', line)
        content = '"%s"' % var.group(1)
        line_content = line_content + content + '\n}'
        line = txt.readline()

    #语句（if、case、赋值）标识
    elif 'NonblockingSubstitution' in line:   #always内非阻塞赋值语句
        block = ''
        nonblockingsubstitution_num += 1
        if else_sign == 'else':      #输出else里的内容，不会进入if的条件
            statement_spacenu_num = block_list_level[-1] * ' '
            line_content = input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right, line_content)
            if line_content == '':
                sysc.write('')
            elif nonblockingsubstitution_num == 1:
                pass
            else:
                sysc.write(statement_spacenu_num + '%s' % line_content)
        else:                     #如果没有else的标志，表示内容是if里的内容，进入if条件
            if sign == 'if':    #if语句
                block_space_num = block_current_num
                statement_spacenu_num = block_current_num * ' '
                line_content = input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right, line_content)
                if bracket_port_num > 1:
                    content = 'if'
                    content1 = '%s\n' % line_content
                    content2 = statement_spacenu_num + '{\n'
                else:
                    content = 'if('
                    content1 = '%s)\n' % line_content
                    content2 = statement_spacenu_num + '{\n'
                line_content = content + content1 + content2
                if ifstatement_num > 1:
                    if ifstatement_space_num > ifstatement_list_if[-1]:
                        if ifelse_sign == 1:
                            sysc.write('%s' % line_content)
                            ifelse_sign = 2
                        elif ifelse_sign == 2:   #if-else已经输出
                            sysc.write('')
                else:
                    sysc.write('')
                # sysc.write(statement_spacenu_num + '%s' % line_content)
        if else_sign == 'else' or sign == 'if':
        # if sign != 'for':
            port_list_right = []
            brackets_symbol_list = []
            port_num, symbol_num, brackets_position, i, bracket_port_num, data_type, bracket_firstport_num, unot_space_num, value_type, sentence_type, ifelse_sign = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            symbol, brackets_symbol, content, content1, content2, line_content, block = '', '', '', '', '', '', ''

        if port_list_right != []:     #等号右端口数组不为空，将数组内的元素个数赋值给port_num
            port_num = len(port_list_right)
            while port_num > 0:   #输出数组元素，即右端口
                if port_num > 1:
                    content = '%s %s' % (port_list_right[i], symbol)
                    i += 1
                    port_num -= 1
                else:
                    if sign == 'for':
                        content = ' %s\n' % port_list_right[i]
                    else:
                        content = ' %s;\n' % port_list_right[i]
                    port_num -= 1
                line_content = line_content + content
            if sign == 'for':
                sysc.write(line_content)
            else:
                sysc.write('    ' + statement_spacenu_num + line_content)
            port_list_right = []
            content, line_content, symbol = '', '', ''
            port_num, i = 0, 0
        port_left_type, port_right_type = '', ''
        sentence_type = 2
        data_type = 0
        plus_identifier_num = 0
        line = txt.readline()
    elif 'BlockingSubstitution' in line:   #always内阻塞赋值语句
        sentence_type = 2
        line = txt.readline()
    elif 'IfStatement' in line:    #always里if语句
        ifstatement_num += 1
        var = re.search('(\s+)IfStatement', line)  # 匹配block前的空格数
        ifstatement_current_num = var.group(1).count(' ')    #当前IfStatement前的空格数
        ifstatement_space_num = ifstatement_current_num
        if ifstatement_num > 1:   #当IfStatement不是第一个时需要判断该IfStatement是否是else
            if ifstatement_space_num > ifstatement_list_if[-1]:
                if block != 'Block':
                    statement_spacenu_num = block_list_level[-1] * ' '
                    sysc.write(statement_spacenu_num + '}\n' + statement_spacenu_num + 'else ')
                    ifstatement_list_if.append(ifstatement_space_num)
                    del (block_list_level[-1])
                    ifelse_sign = 1    #给if-else加一个标志
                    space_num = space_num - 4
                    statement_spacenu_num = space_num * ' '
            elif ifstatement_space_num == ifstatement_list_if[-1]:
                sysc.write('')
        ifstatement_list_if.append(ifstatement_space_num)
        sign = 'if'
        sentence_type = 1
        value_type = 0
        port_left = ''
        line = txt.readline()
    elif 'Case:' in line:    #case语句
        if port_list_right != []:
            port_num = len(port_list_right)
            while port_num > 0:
                if port_num > 1:
                    content = '%s %s' % (port_list_right[i], symbol)
                    i += 1
                    port_num -= 1
                else:
                    content = '%s;\n' % port_list_right[i]
                    port_num -= 1
                line_content = line_content + content
            sysc.write('    ' + statement_spacenu_num + line_content)
            port_list_right = []
            content, line_content, symbol = '', '', ''
            port_num, i = 0, 0
        case_num += 1
        if case_num > 1:
            if sign == 'if':    #if语句
                while block_list_level[-1] > block_list_case[-1]:
                    statement_spacenu_num = block_list_level[-1] * ' '
                    sysc.write(statement_spacenu_num + '}\n')
                    del (block_list_level[-1])
                statement_spacenu_num = block_list_level[-1] * ' '
                sysc.write(statement_spacenu_num + '    break;\n' + statement_spacenu_num + '}\n')
                del (block_list_level[-1])
                # if block_list_if != []:
                #     while block_list_level[-1] >= block_list_if[-1]:
                #         statement_spacenu_num = (block_list_level[-1] - 4) * ' '
                #         sysc.write(statement_spacenu_num + '}\n')
                #         del (block_list_level[-1])
                # else:
                #     statement_spacenu_num = (block_list_level[-1] - 4) * ' '
                #     sysc.write(statement_spacenu_num + '}\n')
                #     del (block_list_level[-1])
            else:
                if sentence_type == 1:
                    while block_list_level[-1] > block_list_case[-1]:
                        statement_spacenu_num = block_list_level[-1] * ' '
                        sysc.write(statement_spacenu_num + '}\n')
                        del (block_list_level[-1])
                    statement_spacenu_num = block_list_level[-1] * ' '
                    sysc.write(statement_spacenu_num + '    break;\n' + statement_spacenu_num + '}\n')
                    del (block_list_level[-1])
                    # if block_list_if != []:
                    #     while block_list_level[-1] >= block_list_if:
                    #         statement_spacenu_num = (block_list_level[-1] - 4) * ' '
                    #         sysc.write(statement_spacenu_num + '}\n')
                    #         del (block_list_level[-1])
                    # else:
                    #     statement_spacenu_num = (block_list_level[-1] - 4) * ' '
                    #     sysc.write(statement_spacenu_num + '}\n')
                    #     del (block_list_level[-1])
                # elif sentence_sign == 'function':
                #     sysc.write('    ' + statement_spacenu_num + 'break;\n' + statement_spacenu_num + '}\n')
                #     space_num = space_num - 4
                else:
                    if lvalue_selection_port != '':
                        sysc.write('    ' + statement_spacenu_num + '%s = %s;\n' % (port_left, lvalue_selection_port))
                        lvalue_selection_port = ''
                        sysc.write('    ' + statement_spacenu_num + 'break;\n' + statement_spacenu_num + '}\n')
                    else:
                        sysc.write('    ' + statement_spacenu_num + 'break;\n' + statement_spacenu_num + '}\n')
                    del (block_list_level[-1])
        sentence_type = 3       #case语句
        port_left_type, port_right_type = '', ''
        value_type, sign, line_content, content, content1 = 0, 0, 0, 0, 0
        line = txt.readline()
    elif 'CaseStatement' in line:    #case部分中的switch语句
        sentence_type = 4
        casestatement = 'casestatement'
        # value_type, data_type = 0, 0
        # portdefine_type = ''
        var = re.search('at (\d+)', line)
        line_num = int(var.group(1))  # 读取当前的行数
        if line_num != linenum and linenum != 0:  # 行数不同，换行输出上一行内容
            linenum = line_num  # 将当前行数赋给存储行数
            i = 0
            line_content = input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right, line_content)
            if block != 'Block':
                if sentence_sign == 'function':
                    sysc.write("%s\n{" % line_content)
                    sysh.write("%s;\n" % line_content)
                else:
                    sysc.write(line_content)  # 输出上一行内容
            port_list_right = []
            port_list_width = []
            brackets_symbol_list = []
            port_num, symbol_num, brackets_position, i, bracket_port_num, data_type, bracket_firstport_num, value_type, unot_space_num, value_type = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # 将变量重新初始化
            symbol, brackets_symbol, content, content1, line_content, portdefine_type = '', '', '', '', '', ''
        line = txt.readline()
    elif 'EventStatement' in line:    #整个case部分结束，在末尾输出default
        statement_spacenu_num = block_list_level[-1] * ' '
        sysc.write('    ' + statement_spacenu_num + 'default:\n')
        statement_spacenu_num = block_list_level[-1] * ' '
        sysc.write('        ' + statement_spacenu_num+'break;\n')
        case_num, sentence_type = 0, 0
        case_intconst = ''
        line = txt.readline()

    #if else层次划分处理
    elif 'Block' in line:
        partselect_num = 0
        and_symbol_num = 0
        nonblockingsubstitution_num = 0
        var = re.search('(\s+)Block', line)   #匹配block前的空格数
        block_current_num = var.group(1).count(' ')
        space_num = space_num + 4
        block = 'Block'
        else_sign = ''
        # if case_num != 0:
        #     statement_spacenu_num = block_list_level[-1] * ' '
        #     sysc.write(statement_spacenu_num + 'case %s:\n' % content1)

        if sentence_type == 1:    #if语句
            block_space_num = block_current_num
            statement_spacenu_num = block_current_num * ' '
            block_list_level.append(block_space_num)
            block_list_if.append(block_space_num)
            bracket_port_num = len(port_list_right)
            line_content = input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right, line_content)
            if bracket_port_num > 1:
                content = 'if'
                content1 = '%s\n' % line_content
            else:
                content = 'if('
                content1 = '%s)\n' % line_content
            line_content = content + content1
            port_list_right = []
            brackets_symbol_list = []
            port_num, symbol_num, brackets_position, i, bracket_port_num, data_type, bracket_firstport_num, unot_space_num, value_type = 0, 0, 0, 0, 0, 0, 0, 0, 0
            symbol, brackets_symbol, content, content1 = '', '', '', ''
            if ifstatement_num > 1:
                if ifelse_sign == 1:
                    sysc.write('%s' % line_content)
                    ifelse_sign = 2
                elif ifelse_sign == 2:  # if-else已经输出
                    # sysc.write('')
                    pass
                else:
                    sysc.write(statement_spacenu_num + '%s' % line_content)
            else:
                sysc.write(statement_spacenu_num + '%s' % line_content)
        elif sentence_type == 3:     #case语句
            if case_intconst == '':     #输出case的default
                sysc.write(statement_spacenu_num + 'default:\n')
            case_intconst = ''
            if block_list_if == []:
                block_space_num = block_current_num
                block_list_level.append(block_space_num)
                # sysc.write("")
            else:
                pass

        if block_space_num == 0:  # 第一个block，只输出"{"
            block_space_num = block_current_num
            if sentence_sign == 'function':
                line_content = input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right, line_content)
                sysc.write("%s\n{\n" % line_content)
            else:
                # statement_spacenu_num = space_num * ' '
                sysc.write('{\n')
            block_list_level.append(block_space_num)
        else:
            if sentence_type == 1:    #判断是否if后的第一个block
                block_space_num = block_current_num
                statement_spacenu_num = block_list_level[-1] * ' '
                sysc.write(statement_spacenu_num + '{\n')
            else:
                if block_current_num > block_list_level[-1]:  # 当前block空格数大于列表里最后一个元素，说明出现更低一层的层次，输出"{"
                    block_space_num = block_current_num
                    block_list_level.append(block_space_num)
                    if case_num == 1:
                        block_list_case.append(block_space_num)
                    statement_spacenu_num = block_current_num * ' '
                    sysc.write(statement_spacenu_num+'{\n')
                elif block_current_num == block_list_level[-1]:  # 当前block空格数与block列表里最后一个相同，说明两个block是同层，前一个block内容结束，输出”}“，同时输出新的"{"
                    # statement_spacenu_num = space_num * ' '
                    statement_spacenu_num = block_current_num * ' '
                    if block_list_if != []:  #
                        if block_current_num == block_list_if[-1]:     #输出else
                            statement_spacenu_num = block_current_num * ' '
                            sysc.write(statement_spacenu_num+'}\n')
                            if casestatement == 'casestatement':
                                statement_spacenu_num = block_current_num * ' '
                                sysc.write(statement_spacenu_num+'else\n' + statement_spacenu_num+'{\n')
                                casestatement = ''
                            else:
                                sysc.write(statement_spacenu_num + 'else\n' + statement_spacenu_num + '{\n')
                            else_sign = 'else'
                            del (block_list_if[-1])
                        else:
                            statement_spacenu_num = block_current_num * ' '
                            sysc.write(statement_spacenu_num + '{\n')
                    else:
                        statement_spacenu_num = block_current_num * ' '
                        sysc.write(statement_spacenu_num + '{\n')

                else:
                    # 当前block空格数小于block列表里最后一个，说明当前block比前一个block层次要高，说明前面block内容结束，将当前block空格数与block列表最后一个元素往回比较，只要是小于一次就输出一次对应层级的“}”
                    # 并删除列表最后一个元素，直到两者相等，结束循环
                    while block_current_num < block_list_level[-1]:
                        space_num = space_num - 4
                        statement_spacenu_num = block_list_level[-1] * ' '
                        if case_num != 0:
                            pass
                        else:
                            sysc.write(statement_spacenu_num+'}\n')
                        del (block_list_level[-1])
                    if block_current_num == block_list_if[-1]:
                        sysc.write(statement_spacenu_num+'else' + statement_spacenu_num+'{\n')
                        del (block_list_if[-1])
                    else:
                        sysc.write(statement_spacenu_num+'{\n')

        line_content = ''
        # port_list_right = []
        brackets_symbol_list = []
        symbol_list = []
        port_num, symbol_num, brackets_position, i, bracket_port_num, data_type, bracket_firstport_num, unot_space_num, value_type, sentence_type, var, always_type = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        symbol, brackets_symbol, content, content1, sens_sign = '', '', '', '', ''
        line = txt.readline()
    else:
        line = txt.readline()
        '''
        if line == '\n':   #出现空行，跳过，继续读取下一行
            line = txt.readline()
        else:      #出现未能识别的关键字，输出整句话并报错
            line = line + ' error!!\n'
            sysc.write(line)
            line = txt.readline()
        '''

sysh.write(hpp_port_content)
sysh.write(hpp_assign_content)
sysh.write(hpp_always_content)

read_state = 'end'

#所有内容读取完毕后，输出最后一个行的内容
i = 0
if data_type != 2:
    bracket_port_num = len(port_list_right)
else:
    pass
if port_list_right != []:
    line_content = input(brackets_symbol_list, brackets_position, i, bracket_port_num, port_list_right, line_content)
if sign == 'if':   #if语句
    statement_spacenu_num = block_list_level[-1] * ' '
    sysc.write(statement_spacenu_num + '%s' % line_content)
    if lvalue_selection_port != '':
        sysc.write('    %s = %s;\n' % (port_left, lvalue_selection_port))
        lvalue_selection_port = ''
else:
    if symbol == '()':   #function调用语句
        sysc.write("}\n")
    elif casestatement == 'casestatement':   #case语句结束后输出跟switch的右括号
        statement_spacenu_num = block_list_level[-1] * ' '
        sysc.write(statement_spacenu_num + '}\n')
    elif instance_name != '':
        pass
    elif line_content == 0:
        pass
    else:
        sysc.write('%s' % line_content)
port_list_right = []
port_list_width = []
brackets_symbol_list = []
port_num, symbol_num, brackets_position, i, bracket_port_num, data_type, bracket_firstport_num, value_type, unot_space_num, value_type = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # 将变量重新初始化
symbol, brackets_symbol, content, content1, line_content = '', '', '', '', ''

#所有内容读取完毕后，输出case的内容
if sentence_sign == 'function':   #function语句
    sysc.write('    ' + statement_spacenu_num + "break;\n")
    while block_list_level != []:
        statement_spacenu_num = block_list_level[-1] * ' '
        sysc.write(statement_spacenu_num + "}\n")
        del (block_list_level[-1])
    sysc.write(statement_spacenu_num + 'return %s;\n}\n' % function_name)   #function函数的返回值
    sentence_sign = ''

#所有内容读取完毕，统计block_list_level中元素个数，在cpp中输出对应个数和层级的"}"
if block_list_level != []:
    statement_spacenu_num = (block_list_level[-1]) * ' '
    if case_num != 0:
        sysc.write(statement_spacenu_num + "    break;\n" + statement_spacenu_num + "}\n")
        del (block_list_level[-1])
    # else:
    #     sysc.write(statement_spacenu_num + "}\n")
    # del (block_list_level[-1])
while block_list_level != []:
    statement_spacenu_num = block_list_level[-1] * ' '
    if len(block_list_level) == 1:
        sysc.write("}\n")
    else:
        sysc.write(statement_spacenu_num+"}\n")
    del (block_list_level[-1])
# if sentence_sign == 'assign':
#     sysc.write('}\n')

#在hpp里输出模块实例化的内容
assign_sumnum = assign_num
instance_sumnum = instance_num
assignlist_num = 1
instancelist_num = 1
# sysh.write("\n\tSC_CTOR(%s)\n\t{\n" % module_name)
if instance_num != 0:  # 输出实例化的端口绑定
    while i < len(instance_object_name_list):   #实例化对象
        if i == 0:
            sysh.write('\n\tSC_CTOR(%s):\n\t\t%s("%s")\n' % (module_name, instance_object_name_list[i], instance_object_name_list[i]))
        else:
            sysh.write('\t\t, %s("%s")\n' % (instance_object_name_list[i], instance_object_name_list[i]))
        i += 1
    sysh.write("\n\t{\n")
    i = 0

    while i < len(instance_object_name_list): #实例化端口绑定
        instancelist = names['instance' + str(instancelist_num)]
        portarglist = names['portarg' + str(instancelist_num)]
        while j < len(portarglist):
            if j == 0:
                # sysh.write('\t\t%s %s("%s");\n' % (instance_module_name_list[i], instance_object_name_list[i], instance_object_name_list[i]))
                if paramarg_content_list != []:
                    sysh.write("\t\t%s\n" % paramarg_content_list[0])
                    del(paramarg_content_list[0])
                else:
                    sysh.write("")
                sysh.write("\t\t%s.%s(%s);\n" % (instance_object_name_list[i], portarglist[j], instancelist[j]))
            else:
                sysh.write("\t\t%s.%s(%s);\n" % (instance_object_name_list[i], portarglist[j], instancelist[j]))
            j += 1
        sysh.write("\n")
        i += 1
        j = 0
        instancelist_num += 1
    i = 0
else:
    sysh.write("\n\tSC_CTOR(%s)\n\t{\n" % module_name)

#在hpp里输出assign的敏感信号内容
while assignlist_num <= assign_sumnum:
    assignlist = {}.fromkeys(names['assign' + str(assignlist_num)]).keys()
    assignlist = list(assignlist)
    while i < len(assignlist):
        if i == 0:
            sysh.write("\t\tSC_METHOD(assign_%s);\n\t\tsensitive" % assignlist[i])
        elif i == 1:
            if function_name in assignlist:
                sysh.write("")
            else:
                sysh.write(" << %s" % assignlist[i])
        else:
            sysh.write(" << %s" % assignlist[i])
        i += 1
    sysh.write(";\n")
    i = 0
    assignlist_num += 1

#在hpp里输出always的敏感信号内容
always_sumnum = always_num
alwayslist_num = 1
sens_num = 0
# i = 0
while alwayslist_num <= always_sumnum:
    alwayslist = {}.fromkeys(names['always' + str(alwayslist_num)]).keys()
    alwayslist= list(alwayslist)
    if names['sensalways' + str(alwayslist_num)] == []:     #时序逻辑
        if names['posedgelist' + str(alwayslist_num)] != []:
            pos_num = len(names['posedgelist' + str(alwayslist_num)])
            while pos_num > 0:
                if sens_num == 0:
                    sysh.write("\t\tSC_METHOD(always_block%s);\n\t\tsensitive << %s.pos()" % (alwayslist_num, names['posedgelist' + str(alwayslist_num)][i]))
                elif sens_num == 1:   #该时序电路含有两个上升沿触发
                    sysh.write(" << %s.pos()" % names['posedgelist' + str(alwayslist_num)][i])
                pos_num -= 1
                sens_num += 1
        else:     #没有上升沿触发信号
            sysh.write('')

        if names['negedgelist' + str(alwayslist_num)] == []:
            sysh.write('')
        else:
            if sens_num == 1:    #前面已经输出了上升沿触发信号
                sysh.write(" << %s.neg()" % names['negedgelist' + str(alwayslist_num)][i])
            elif sens_num == 0:   #前面没有上升沿触发信号
                neg_num = len(names['negedgelist' + str(alwayslist_num)])
                while neg_num > 0:
                    if sens_num == 0:
                        sysh.write("\t\tSC_METHOD(always_block%s);\n\t\tsensitive << %s.neg()" % (alwayslist_num, names['negedgelist' + str(alwayslist_num)][i]))
                    elif sens_num == 1:
                        sysh.write(" << %s.neg()" % names['negedgelist' + str(alwayslist_num)][i])
                    neg_num -= 1
                    sens_num += 1
                    i += 1

        sens_num = 0

    else:          #组合逻辑
        while i < len(alwayslist):
            if i == 0:
                sysh.write("\t\tSC_METHOD(always_combilogic_block%s);\n\t\tsensitive << %s" % (alwayslist_num, alwayslist[i]))
                i += 1
            else:
                sysh.write(" << %s" % alwayslist[i])
                i += 1
    sysh.write(";\n")
    i = 0
    alwayslist_num += 1

if assignlist_num == assign_sumnum + 1:
    sysh.write("\t\t}\n")
sysh.write("};")


#将Verilog模块名存入sys_py文件，后续在自动生成testbeach时进行调用
#sys_py.write('modulename = "%s"' % module_name)
#sys_py.close()

sysh.seek(0)
print(sysh.read())
sysc.seek(0)
print(sysc.read())

# time_end = time.time()
# print('totally cost', time_end-time_start)
