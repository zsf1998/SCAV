import re
import sys
##命令行部分
SCast_file = sys.argv[1]
new_ast_code  = open("%s.v"%SCast_file[:-4], 'a+')

##测试部分
# SCast_file = "test_new.txt"
# SCast_file = "func_test_new.txt"
# SCast_file = "sm3_control_new.txt"
# SCast_file = "Ternary_operator_new.txt"
# SCast_file = "2_new.txt"
# SCast_file = "full_adder1_new.txt"
# SCast_file = "messagecompress1_new.txt"
# SCast_file = "half_adder_new.txt"
# SCast_file = "even_divide3_new.txt"
# SCast_file = "s_to_p_new.txt"
# SCast_file = "moore_fsm_new_new.txt"

new_ast_code  = open(SCast_file[:-4]+".v", 'a+')

f_ast= open(SCast_file, 'r')



new_ast_code.truncate(0)
regx_Dumping=re.compile("Dumping (\w+)\:\n")
regx_FieldDecl=re.compile("FieldDecl +<(.*)> col:\d+ +(\w+) +'(.*?)'")
regx_Finish_FieldDecl=re.compile("CXXOperatorCallExpr  <line:\d+:\d+, col:\d+> 'void' '()'")
regx_FieldDecl_num=re.compile("\d+")
regx_VarDecl=re.compile("VarDecl.*used (\w+) '(\w+)'")
regx_CXXOperatorCallExpr=re.compile("CXXOperatorCallExpr .* '(.*)' adl") ##非等号情况
regx_CXXOperatorCallExpr1=re.compile("CXXOperatorCallExpr .* '(.*)'")  ##等号赋值情况
regx_CXXOperatorCallExpr2=re.compile("(.*)CXXOperatorCallExpr")
regx_CXXOperatorCallExpr3=re.compile("(.*)CXXOperatorCallExpr  <line:")
regx_MaterializeTemporaryExpr=re.compile("MaterializeTemporaryExpr  ' lvalue")
regx_ConditionalOperator=re.compile("(.*)ConditionalOperator")
regx_CXXBindTemporaryExpr=re.compile("(.*)CXXBindTemporaryExpr")
regx_CXXMethodDecl=re.compile("CXXMethodDecl.*function_.* '\w+<(\d+)> .*<(\d+)>.*'")
regx_none=re.compile("\n")
regx_MemberExpr=re.compile("MemberExpr +(\w+)")
regx_MemberExpr1=re.compile("MemberExpr  ' lvalue (.*)")
regx_MemberExpr2=re.compile("MemberExpr  ' .range")
regx_CXXOperatorCallExpr4=re.compile("CXXOperatorCallExpr   '.*' lvalue '\[\]'")
regx_IntegerLiteral=re.compile("IntegerLiteral .* (\w+)")
regx_IntegerLiteral1=re.compile("0x(\w+)")
regx_IntegerLiteral2=re.compile("=0x(\w+)")
regx_BinaryOperator=re.compile("BinaryOperator +(.*) +'(.*)'")
regx_ParenExpr=re.compile("ParenExpr")
regx_ParmVarDecl=re.compile("ParmVarDecl *(\w+) '\w+<(\d+)>':.*")
regx_UnaryOperator=re.compile("UnaryOperator.* '(\W+)'")
regx_IfStmt=re.compile("(.*)IfStmt")
regx_IfStmt_else=re.compile("(.*)IfStmt   has_else")
regx_CompoundStmt=re.compile("(.*)CompoundStmt")
regx_SwitchStmt=re.compile("(.*)SwitchStmt")
regx_CaseStmt=re.compile("(.*)CaseStmt")
regx_ForStmt=re.compile("ForStmt")
regx_ExprWithCleanups=re.compile("(.*)ExprWithCleanups")
regx_ExprWithCleanups1=re.compile("(.*)ExprWithCleanups  <line:")
regx_RecoveryExpr=re.compile("RecoveryExpr")
regx_RecoveryExpr1=re.compile("RecoveryExpr  <line:")
regx_wire=re.compile("wire.* (\w+)")
regx_io_reg=re.compile("(input|output|inout) .* (\w+)")
regx_BreakStmt=re.compile("(.*)BreakStmt")
regx_DefaultStmt=re.compile("DefaultStmt")
regx_ImplicitCastExpr=re.compile("ImplicitCastExpr")
regx_ReturnStmt=re.compile("ReturnStmt")
regx_CXXBindTemporaryExpr=re.compile("(.*)CXXBindTemporaryExpr")
regx_var=re.compile("var_(\w+)")

regx_conti_colon=re.compile("(:)(?=\n *\w+:)")
regx_pos=re.compile("pos:(.*)")
regx_neg=re.compile("neg:(.*)")
regx_sensitive=re.compile("sensitive:(.*);(.*)")
pos=""
neg=""
always_block_num=1
assign_sign=0
assign_first=0
compoundstmt=0
bracket_sign=0

FieldDecl_cont=""
function_signal=""
function_signal_width=0
function_array=[]
module_port=""
finish_write_port=0
new_line_iden=0
Lvalue=""
operator=[]
member=[]
IntegerLiteral=[]
one_IntegerLiteral=0
range_sign=0
ImplicitCastExpr_sign=0
member_sign=0
merge_operator=1
instantiation_content=""
instantiation_modules=[]
instantiation_num=0
recent_instantiation=""
instantiation_first=""
finish_content=""
joint_sign=-1
judge_colon=0
sign_fist=""
new_member=""
operator_first=""
if_sign=0
if_space=[]
content_if=""
always_sign=0
always_first=0
always_output_sign=0
always_function=0
judge_num=0
swich_sign=0
case_sign=0
case_sign1=0
case_space=0
endcase_sign=0
endcase_space=0
for_sign=0
assign_content=""
always_content=""
statement_assign_sign=0
num_contains=0
a=0
wire_sign=[]
reg_sign=[]
FieldDecl_cont_new=""
new_always_content=""
select_operator=0
ternary_sign=0
len_ternary=0
ternary_content=""

space=''
has_else=0
else_space=[]
begin_end=[]
recent_space=0
recent_space1=0
always_sensitive=[]
always=[]

always_combilogic=0
pp=0
instantiation=0

function_in=""
returnstmt_sign=0

ConditionalOperator_sign=0
member1=[]
operator1=[]
member5=[]
member3=[]
member4=[]
operator3=[]
operator4=[]
operator5=[]
one_sign=0
two_sign=0
member_last=""
always_first_port=""
always_firstport=0
var_member=[]

##合并member中最后两个数组,operator_first在合并之后清零
def joint():
    global joint_sign
    global member
    global operator_first
    if joint_sign == 0:
        joint_sign=-1
        member1 = member[-1]
        member2 = member[-2]
        if member2==":" or member1==":" :
            operator_first = ""
            return
        member = member[:-2]
        if operator_first==",":
            member.append("{%s,%s}" % (member2, member1))
        # elif operator_first=="<"or operator_first==">":
        #     member.append("{%s,%s}" % (member2, member1))
        else:
            # pass
            member.append("(%s%s%s)" % (member2,operator_first, member1))
        operator_first=""
        # print("___", member)
        return

##一行语句结束时的输出函数
def end_output_always():
    global member,operator,always_content,IntegerLiteral,one_IntegerLiteral,merge_operator,finish_content,last_member,new_member,recent_space
    if member:
        joint()

        # print(operator)
        # member = member[1:]
        if len(operator) == 1 and operator[-1] == ";":
            member.insert(1000,operator[-1])
        else:
            for i in range(len(operator)):
                member.insert(merge_operator, operator[i])
                merge_operator = merge_operator + 2
        print(member)

        for i in range(len(member)):
            finish_content = finish_content + member[i]
        print(finish_content)
        always_content = always_content +recent_space*" "+ finish_content + "\n"

    operator = []
    member = []
    IntegerLiteral = []
    one_IntegerLiteral = 0
    merge_operator = 1
    finish_content = ""
    last_member = ""
    new_member = ""

##进行三元操作符合并
def ternary_joint(member_1,operator_1):
    len_member_1 = 0
    len_member_1 = len(member_1)
    content=""
    for j in range(len(member_1)):
        if j == len(operator_1):
            content = content + member_1[j]
            print("_________content:", content)
            break
        else:
            content = content + member_1[j] + operator_1[j]
    if len(operator_1)>=1:
        return "("+content+")"
    else:
        return content

names=locals()

for line in f_ast.readlines():
    if ImplicitCastExpr_sign==2:
        ImplicitCastExpr_sign=1
    elif ImplicitCastExpr_sign==1:
        ImplicitCastExpr_sign=0
    if member_sign==2:
        member_sign=1
    elif member_sign==1:
        member_sign=0
    ##always部分
    if always_sign==1:
        if regx_IfStmt.search(line):
            if if_sign==0 and swich_sign!=1 and len(member):
                operator.append(";")
                end_output_always()
            regx_IfStmt_obj=regx_IfStmt.search(line)

            recent_space1=recent_space
            recent_space=len(regx_IfStmt_obj.group(1))
            if_space.append(len(regx_IfStmt_obj.group(1)))
            content_if = (recent_space-2)*" "+"if("
            if_sign = 1
            print("_____________________", str(len(regx_IfStmt_obj.group(1))))

            if len(else_space):
                if recent_space==(else_space[-1][1]+2):
                    if else_space[-1][0]==1:
                        always_content = always_content + (begin_end[-1]) * " " + "end\n"
                        begin_end.pop()
                        content_if = (recent_space1 - 2) * " " + "else if("
                        else_space[-1][0]=2
                        else_space[-1][1]=else_space[-1][1]+2
                else:
                    if "has_else" in line:
                        else_space.append([2, len(regx_IfStmt_obj.group(1))])
                        print("+++++++++++++++++++++++++++++++++++++++++", else_space)

            if "has_else" in line:
                if len(else_space):
                    if recent_space==(else_space[-1][1]+2):
                        if else_space[-1][0]==1:
                            content_if = (recent_space1 - 2) * " " + "else if("
                            else_space[-1][0]=2
                            else_space[-1][1] = else_space[-1][1] + 2
                else:
                    has_else=2
                    else_space.append([2,len(regx_IfStmt_obj.group(1))])
                    print("+++++++++++++++++++++++++++++++++++++++++",else_space)

        elif regx_ParmVarDecl.search(line):
            regx_ParmVarDecl_obj=regx_ParmVarDecl.search(line)
            function_in="%s"%regx_ParmVarDecl_obj.group(1)
            always_content="input [%s:0]"%(int(regx_ParmVarDecl_obj.group(2))-1)+always_content+function_in+"\n"


        elif regx_CXXMethodDecl.search(line):
            regx_CXXMethodDecl_obj = regx_CXXMethodDecl.search(line)
            if always_function == 1:
                always_tir = "\nfunction [%s,0] %s" % (
                int(regx_CXXMethodDecl_obj.group(1)) - 1, "func_" + regx_Dumping_function_obj.group(1))



        elif regx_ConditionalOperator.search(line):
            regx_ConditionalOperator_obj=regx_ConditionalOperator.search(line)
            select_operator = 3
            ConditionalOperator_sign = 1
            ternary_sign = 3
            len_ternary = len(regx_ConditionalOperator_obj.group(1))

        elif regx_CXXBindTemporaryExpr.search(line):
            regx_CXXBindTemporaryExpr_obj = regx_CXXBindTemporaryExpr.search(line)
            if len(regx_CXXBindTemporaryExpr_obj.group(1)) == (len_ternary + 2):
                if ternary_sign == 3:
                    ternary_sign = 4
                elif ternary_sign == 4:
                    ternary_sign = 5


        elif regx_SwitchStmt.search(line):
            if len(member):
                operator.append(";")
                end_output_always()
            ##对函数的情况额外处理
            if always_function==1:
                content_swich = "case(%s"%function_in
                swich_sign = 1
                recent_space = recent_space + 4
            else:
                regx_CompoundStmt_obj = regx_SwitchStmt.search(line)
                ##对if的两个层次进行判断，如果是第二层就输出else
                if else_space:
                    ##没有else if的情况
                    if else_space[-1][1] == (len(regx_CompoundStmt_obj.group(1)) - 2) and len(begin_end) > 0:
                        if else_space[-1][0] == 1:
                            always_content = always_content + (begin_end[-1]) * " " + "end\n"
                            begin_end.pop()
                            always_content = always_content + (else_space[-1][1] - 2) * " " + "else\n"
                            always_content = always_content + (recent_space) * " " + "begin\n"
                            begin_end.append(recent_space)
                            else_space.pop()
                            if_space.pop()
                        elif len(else_space):
                            else_space[-1][0] = else_space[-1][0] - 1
                content_swich="case("
                swich_sign=1
                recent_space = recent_space + 4

        elif regx_CaseStmt.search(line):
            regx_CaseStmt_obj=regx_CaseStmt.search(line)
            content_case="'d:"
            case_sign=1
            case_sign1=1
            case_space=len(regx_CaseStmt_obj.group(1))

        elif regx_ForStmt.search(line):
            content_for = "for( "
            for_sign=1

        elif regx_CompoundStmt.search(line):
            if if_sign==0 and swich_sign!=1 and for_sign!=1:
                operator.append(";")
                end_output_always()
            regx_CompoundStmt_obj=regx_CompoundStmt.search(line)

            ##if条件判断内容
            # if if_sign==1 and member:
            #     joint()
            #     print(member)
            #     print(operator)
            #     for i in range(len(operator)):
            #         member.insert(merge_operator, operator[i])
            #         merge_operator = merge_operator + 2
            #     print(member)
            #
            #     for i in range(len(member)):
            #         finish_content = finish_content + member[i]
            #
            # if swich_sign==1 and member:
            #     joint()
            #     print(member)
            #     print(operator)
            #     for i in range(len(operator)):
            #         member.insert(merge_operator, operator[i])
            #         merge_operator = merge_operator + 2
            #     print(member)
            #     for i in range(len(member)):
            #         finish_content = finish_content + member[i]
            #
            # if for_sign==1 and member:
            #     joint()
            #     print(member)
            #     print(operator)
            #     for i in range(len(operator)):
            #         member.insert(merge_operator, operator[i])
            #         merge_operator = merge_operator + 2
            #     print(member)
            #     for i in range(len(member)):
            #         finish_content = finish_content + member[i]

            if member:
                if if_sign==1 or swich_sign==1 or for_sign==1 :
                    if len(member)>1:
                        joint()
                    print(member)
                    print(operator)
                    for i in range(len(operator)):
                        member.insert(merge_operator, operator[i])
                        merge_operator = merge_operator + 2
                    print(member)
                    for i in range(len(member)):
                        finish_content = finish_content + member[i]

            #处理if括号里面的内容,添加begin end列表
            if if_sign == 1:
                if_sign = 0
                content_if = content_if +finish_content+ ")"
                always_content=always_content+content_if+"\n"
                always_content=always_content+(recent_space)*" "+"begin\n"
                begin_end.append(recent_space)

                content_if = ""
                operator = []
                member = []
                IntegerLiteral = []
                one_IntegerLiteral = 0
                merge_operator = 1
                finish_content = ""


            elif swich_sign==1:
                swich_sign=0
                content_swich=content_swich+finish_content+")"
                always_content=always_content+recent_space*" "+content_swich+"\n"

                content_swich = ""
                operator = []
                member = []
                IntegerLiteral = []
                one_IntegerLiteral = 0
                merge_operator = 1
                finish_content = ""

                continue

            elif for_sign==1:
                for_sign=0
                content_for=content_for+finish_content+")"
                always_content = always_content + recent_space * " " + content_for + "\n"
                always_content = always_content + (recent_space) * " " + "begin\n"
                begin_end.append(recent_space)

                content_for = ""
                operator = []
                member = []
                IntegerLiteral = []
                one_IntegerLiteral = 0
                merge_operator = 1
                finish_content = ""

                continue

            ##对if的两个层次进行判断，如果是第二层就输出else
            if else_space:
                ##没有else if的情况
                if else_space[-1][1] == (len(regx_CompoundStmt_obj.group(1)) - 2) and len(begin_end) > 0:
                    if else_space[-1][0] == 1:
                        always_content = always_content + (begin_end[-1]) * " " + "end\n"
                        begin_end.pop()
                        always_content = always_content + (else_space[-1][1] - 2) * " " + "else\n"
                        always_content = always_content + (recent_space) * " " + "begin\n"
                        begin_end.append(recent_space)
                        else_space.pop()
                        if_space.pop()
                    elif len(else_space):
                        else_space[-1][0] = else_space[-1][0] - 1
                ##有else if的情况
                elif else_space[-1][1] == (len(regx_CompoundStmt_obj.group(1)) - 4) and len(begin_end) > 0:
                    if else_space[-1][0] == 1:
                        always_content = always_content + (begin_end[-1]) * " " + "end\n"
                        begin_end.pop()
                        always_content = always_content + (else_space[-1][1] - 2) * " " + "else\n"
                        always_content = always_content + (recent_space) * " " + "begin\n"
                        begin_end.append(recent_space)
                        else_space.pop()
                        if_space.pop()
                    elif len(else_space):
                        else_space[-1][0] = else_space[-1][0] - 1

        elif regx_ExprWithCleanups1.search(line):
            select_operator=0
            ConditionalOperator_sign = 1

            if ternary_sign == 5:
                print("3", member3, operator3)
                print("4", member4, operator4)
                print("5", member5, operator5)
                ternary_content =  ternary_content + ternary_joint(member3,
                                                                                   operator3) + "?" + ternary_joint(
                    member4, operator4) + ":" + ternary_joint(member5, operator5) + ";"
                print("always_ternary_content:          ", ternary_content)

            if ternary_sign == 5:
                if always_combilogic==1:
                    always_content = always_content + always_first_port + "<=" + ternary_content + "\n"
                else:
                    always_content = always_content + always_first_port+"<="+ternary_content + "\n"
            else:
                pass
                # assign_content = assign_content + finish_content + "\n"
            member3=[]
            member4=[]
            member5=[]
            operator3=[]
            operator4=[]
            operator5=[]
            ternary_sign=0
            ternary_content = ""



        elif regx_ExprWithCleanups.search(line):
            if if_sign==0 and swich_sign!=1 and for_sign!=1:
                operator.append(";")
                end_output_always()

            regx_CompoundStmt_obj=regx_ExprWithCleanups.search(line)

            ##if条件判断内容
            if member:
                if if_sign == 1 or swich_sign == 1 or for_sign == 1:
                    if len(member) > 1:
                        joint()
                    print(member)
                    print(operator)
                    for i in range(len(operator)):
                        member.insert(merge_operator, operator[i])
                        merge_operator = merge_operator + 2
                    print(member)
                    for i in range(len(member)):
                        finish_content = finish_content + member[i]

            #处理if括号里面的内容,添加begin end列表
            if if_sign == 1:
                if_sign = 0
                content_if = content_if +finish_content+ ")"
                print("+++++", content_if)
                always_content=always_content+content_if+"\n"
                always_content=always_content+(recent_space)*" "+"begin\n"
                begin_end.append(recent_space)

                content_if = ""
                operator = []
                member = []
                IntegerLiteral = []
                one_IntegerLiteral = 0
                merge_operator = 1
                finish_content = ""


            elif swich_sign==1:
                swich_sign=0
                content_swich=content_swich+finish_content+")"
                print("____",content_swich)
                always_content=always_content+recent_space*" "+content_swich+"\n"

                content_swich = ""
                operator = []
                member = []
                IntegerLiteral = []
                one_IntegerLiteral = 0
                merge_operator = 1
                finish_content = ""

                continue

            elif for_sign==1:
                for_sign=0
                content_for=content_for+finish_content+")"
                always_content = always_content + recent_space * " " + content_for + "\n"
                always_content = always_content + (recent_space) * " " + "begin\n"
                begin_end.append(recent_space)

                content_for = ""
                operator = []
                member = []
                IntegerLiteral = []
                one_IntegerLiteral = 0
                merge_operator = 1
                finish_content = ""

                continue

            ##对if的两个层次进行判断，如果是第二层就输出else
            if else_space:
                ##没有else if的情况
                if else_space[-1][1] == (len(regx_CompoundStmt_obj.group(1)) - 2) and len(begin_end) > 0:
                    if else_space[-1][0] == 1:
                        always_content = always_content + (begin_end[-1]) * " " + "end\n"
                        begin_end.pop()
                        always_content = always_content + (else_space[-1][1] - 2) * " " + "else\n"
                        always_content = always_content + (recent_space) * " " + "begin\n"
                        begin_end.append(recent_space)
                        else_space.pop()
                    elif len(else_space):
                        else_space[-1][0] = else_space[-1][0] - 1

        elif regx_UnaryOperator.search(line):
            if if_sign == 1:
                regx_UnaryOperator_obj = regx_UnaryOperator.search(line)
                sign_fist = regx_UnaryOperator_obj.group(1)

        elif regx_BinaryOperator.search(line):
            regx_BinaryOperator_obj = regx_BinaryOperator.search(line)
            if case_sign1 == 1:
                always_content = always_content + (recent_space) * " " + "begin\n"
                begin_end.append(recent_space)
                case_sign1 = 0
            if regx_BinaryOperator_obj.group(2)=="=":
                operator.append(";")
                end_output_always()
                always_first = 1
                if always_combilogic==0 and always_function==0:
                    operator.append("<"+regx_BinaryOperator_obj.group(2))
                elif always_combilogic==1 or always_function==1:
                    operator.append( regx_BinaryOperator_obj.group(2))
            else:
                if regx_BinaryOperator_obj.group(1) == "'bool'":
                    a=1
                if if_sign == 1:
                    if regx_BinaryOperator_obj.group(2)=="==":
                        judge_num=1
                    elif regx_BinaryOperator_obj.group(2)=="<" :
                        judge_num = 2
                    elif regx_BinaryOperator_obj.group(2)==">":
                        judge_num = 3
                    else:
                        operator.append(regx_BinaryOperator_obj.group(2))
                else:
                    if select_operator==3:
                        operator_first=regx_BinaryOperator_obj.group(2)
                    else:
                        operator.append(regx_BinaryOperator_obj.group(2))

            if ternary_sign == 3:
                operator3.append(regx_BinaryOperator_obj.group(2))
            elif ternary_sign == 4:
                operator4.append(regx_BinaryOperator_obj.group(2))
            elif ternary_sign == 5:
                operator5.append(regx_BinaryOperator_obj.group(2))

        elif regx_RecoveryExpr1.search(line):
            operator.append(";")
            end_output_always()
            operator.append("=")


        # elif regx_CXXOperatorCallExpr3.search(line):
        #     if if_sign==0 and swich_sign!=1 and for_sign!=1:
        #         operator.append(";")
        #         end_output_always()
        #
        #     regx_CompoundStmt_obj=regx_CXXOperatorCallExpr3.search(line)
        #     ##if条件判断内容
        #     if member:
        #         if if_sign == 1 or swich_sign == 1 or for_sign == 1:
        #             if len(member) > 1:
        #                 joint()
        #             print(member)
        #             print(operator)
        #             for i in range(len(operator)):
        #                 member.insert(merge_operator, operator[i])
        #                 merge_operator = merge_operator + 2
        #             print(member)
        #             for i in range(len(member)):
        #                 finish_content = finish_content + member[i]
        #
        #     #处理if括号里面的内容,添加begin end列表
        #     if if_sign == 1:
        #         if_sign = 0
        #         content_if = content_if +finish_content+ ")"
        #         print("+++++", content_if)
        #         always_content=always_content+content_if+"\n"
        #         always_content=always_content+(recent_space)*" "+"begin\n"
        #         begin_end.append(recent_space)
        #
        #         content_if = ""
        #         operator = []
        #         member = []
        #         IntegerLiteral = []
        #         one_IntegerLiteral = 0
        #         merge_operator = 1
        #         finish_content = ""
        #
        #     elif swich_sign==1:
        #         swich_sign=0
        #         content_swich=content_swich+finish_content+")"
        #         print("____",content_swich)
        #         always_content=always_content+recent_space*" "+content_swich+"\n"
        #
        #         content_swich = ""
        #         operator = []
        #         member = []
        #         IntegerLiteral = []
        #         one_IntegerLiteral = 0
        #         merge_operator = 1
        #         finish_content = ""
        #         continue
        #
        #     elif for_sign==1:
        #         for_sign=0
        #         content_for=content_for+finish_content+")"
        #         always_content = always_content + recent_space * " " + content_for + "\n"
        #         always_content = always_content + (recent_space) * " " + "begin\n"
        #         begin_end.append(recent_space)
        #
        #         content_for = ""
        #         operator = []
        #         member = []
        #         IntegerLiteral = []
        #         one_IntegerLiteral = 0
        #         merge_operator = 1
        #         finish_content = ""
        #         continue

        elif regx_CXXOperatorCallExpr3.search(line):
            if ternary_sign == 5:
                print("3", member3, operator3)
                print("4", member4, operator4)
                print("5", member5, operator5)
                ternary_content =  ternary_content + ternary_joint(member3,
                                                                                   operator3) + "?" + ternary_joint(
                    member4, operator4) + ":" + ternary_joint(member5, operator5) + ";"
                print("always_ternary_content:          ", ternary_content)

            if ternary_sign == 5:
                if always_combilogic==1:
                    always_content = always_content + always_first_port + "<=" + ternary_content + "\n"
                else:
                    always_content = always_content + always_first_port+"<="+ternary_content + "\n"
            else:
                pass
                # assign_content = assign_content + finish_content + "\n"
            member3=[]
            member4=[]
            member5=[]
            operator3=[]
            operator4=[]
            operator5=[]
            ternary_sign=0
            ternary_content=""
            if regx_CXXOperatorCallExpr1.search(line):
                if if_sign == 0 and swich_sign != 1 and for_sign != 1:
                    operator.append(";")
                    end_output_always()

                ##if条件判断内容
                if member:
                    if if_sign == 1 or swich_sign == 1 or for_sign == 1:
                        if len(member) > 1:
                            joint()
                        print(member)
                        print(operator)
                        for i in range(len(operator)):
                            member.insert(merge_operator, operator[i])
                            merge_operator = merge_operator + 2
                        print(member)
                        for i in range(len(member)):
                            finish_content = finish_content + member[i]
                if if_sign == 1:
                    if_sign = 0
                    content_if = content_if + finish_content + ")"
                    print("+++++", content_if)
                    always_content = always_content + content_if + "\n"
                    always_content = always_content + (recent_space) * " " + "begin\n"
                    begin_end.append(recent_space)

                    content_if = ""
                    operator = []
                    member = []
                    IntegerLiteral = []
                    one_IntegerLiteral = 0
                    merge_operator = 1
                    finish_content = ""

                if for_sign != 1:
                    operator.append(";")
                    end_output_always()
                if case_sign1 == 1:
                    recent_space = case_space
                    always_content = always_content + (recent_space) * " " + "begin\n"
                    begin_end.append(recent_space)
                    case_sign1 = 0

                regx_CXXOperatorCallExpr1_obj = regx_CXXOperatorCallExpr1.search(line)
                if regx_CXXOperatorCallExpr1_obj.group(1) == "=":
                    if always_combilogic == 0 and always_function == 0:
                        operator.append("<" + regx_CXXOperatorCallExpr1_obj.group(1))
                        always_first = 1
                    elif always_combilogic == 1 or always_function == 1:
                        operator.append(regx_CXXOperatorCallExpr1_obj.group(1))
                elif regx_CXXOperatorCallExpr1_obj.group(1) == "++":
                    pp = 1
                regx_CompoundStmt_obj = regx_CXXOperatorCallExpr2.search(line)

                ##限制只有两个com也就是if else的第二个com的时候才要输出end
                if else_space:
                    if else_space[-1][1] == (len(regx_CompoundStmt_obj.group(1)) - 2) and len(begin_end) > 0:
                        if else_space[-1][0] == 1:
                            always_content = always_content + (begin_end[-1]) * " " + "end\n"
                            begin_end.pop()
                            always_content = always_content + (else_space[-1][1] - 2) * " " + "else\n"
                            always_content = always_content + (recent_space) * " " + "begin\n"
                            begin_end.append(recent_space)
                            else_space.pop()
                        elif len(else_space):
                            else_space[-1][0] = else_space[-1][0] - 1



        elif regx_CXXOperatorCallExpr4.search(line):
            print("++++++++++++")
            one_sign = 1

        elif regx_ParenExpr.search(line):
            if one_IntegerLiteral == 1:
                last_member = member[-1]
                member = member[:-1]
                last_member = last_member + "]"
                member.append(last_member)
                one_IntegerLiteral = 0

            joint()
            joint_sign = 2
            bracket_sign = 1

        elif regx_CXXOperatorCallExpr.search(line):
            regx_CXXOperatorCallExpr_obj = regx_CXXOperatorCallExpr.search(line)
            # joint()
            if one_IntegerLiteral == 1:
                last_member = member[-1]
                member = member[:-1]
                last_member = last_member + "]"
                member.append(last_member)
                one_IntegerLiteral = 0

            if regx_CXXOperatorCallExpr_obj.group(1) == "," or regx_CXXOperatorCallExpr_obj.group(1) == "&":
                operator_first = regx_CXXOperatorCallExpr_obj.group(1)
            else:
                operator.append(regx_CXXOperatorCallExpr_obj.group(1))

        elif regx_CXXOperatorCallExpr.search(line):
            regx_CXXOperatorCallExpr_obj=regx_CXXOperatorCallExpr.search(line)
            operator.append(regx_CXXOperatorCallExpr_obj.group(1))


        elif regx_CXXOperatorCallExpr1.search(line):
            if if_sign==0 and swich_sign!=1 and for_sign!=1:
                operator.append(";")
                end_output_always()

            ##if条件判断内容
            if member:
                if if_sign == 1 or swich_sign == 1 or for_sign == 1:
                    if len(member) > 1:
                        joint()
                    print(member)
                    print(operator)
                    for i in range(len(operator)):
                        member.insert(merge_operator, operator[i])
                        merge_operator = merge_operator + 2
                    print(member)
                    for i in range(len(member)):
                        finish_content = finish_content + member[i]
            if if_sign==1:
                if_sign = 0
                content_if = content_if +finish_content+ ")"
                print("+++++", content_if)
                always_content=always_content+content_if+"\n"
                always_content=always_content+(recent_space)*" "+"begin\n"
                begin_end.append(recent_space)

                content_if = ""
                operator = []
                member = []
                IntegerLiteral = []
                one_IntegerLiteral = 0
                merge_operator = 1
                finish_content = ""



            if for_sign!=1:
                operator.append(";")
                end_output_always()
            if case_sign1==1:
                recent_space=case_space
                always_content=always_content+(recent_space)*" "+"begin\n"
                begin_end.append(recent_space)
                case_sign1=0

            regx_CXXOperatorCallExpr1_obj=regx_CXXOperatorCallExpr1.search(line)
            if regx_CXXOperatorCallExpr1_obj.group(1)=="=":
                if always_combilogic==0 and always_function==0:
                    operator.append("<"+regx_CXXOperatorCallExpr1_obj.group(1))
                    always_first=1
                elif always_combilogic==1 or always_function==1:
                    operator.append(regx_CXXOperatorCallExpr1_obj.group(1))
            elif regx_CXXOperatorCallExpr1_obj.group(1)=="++":
                pp=1
            regx_CompoundStmt_obj = regx_CXXOperatorCallExpr2.search(line)

            ##限制只有两个com也就是if else的第二个com的时候才要输出end
            if else_space:
                if else_space[-1][1] == (len(regx_CompoundStmt_obj.group(1)) - 2) and len(begin_end) > 0:
                    if else_space[-1][0] == 1:
                        always_content = always_content + (begin_end[-1]) * " " + "end\n"
                        begin_end.pop()
                        always_content = always_content + (else_space[-1][1] - 2) * " " + "else\n"
                        always_content = always_content + (recent_space) * " " + "begin\n"
                        begin_end.append(recent_space)
                        else_space.pop()
                    elif len(else_space):
                        else_space[-1][0] = else_space[-1][0] - 1

        elif regx_MemberExpr2.search(line):
            two_sign = 2

        elif regx_MemberExpr.search(line):
            if returnstmt_sign==1:
                pass
            else:
                regx_MemberExpr_obj = regx_MemberExpr.search(line)
                if always_firstport==1:
                    always_first_port=always_first_port+regx_MemberExpr_obj.group(1)
                    always_firstport=0
                if always_first==1 :
                    if regx_MemberExpr_obj.group(1) not in reg_sign:
                        reg_sign.append(regx_MemberExpr_obj.group(1))
                        always_first=2
                    else:
                        always_first = 2
                if always_combilogic==1 :
                    if regx_MemberExpr_obj.group(1) not in reg_sign:
                        reg_sign.append(regx_MemberExpr_obj.group(1))
                if pp==1:
                    finish_content=finish_content+"%s=%s+1"%(regx_MemberExpr_obj.group(1),regx_MemberExpr_obj.group(1))

                    operator = []
                    member = []
                    IntegerLiteral = []
                    one_IntegerLiteral = 0
                    merge_operator = 1
                    continue

                if if_sign == 1 or swich_sign==1 or for_sign==1:
                    if len(member) > 1:
                        joint()

                    if sign_fist:
                        new_member = sign_fist + regx_MemberExpr_obj.group(1)
                        sign_fist = ""
                    else:
                        new_member = regx_MemberExpr_obj.group(1)


                    member.append(new_member)
                    # member.append(regx_MemberExpr_obj.group(1))

                    if one_IntegerLiteral == 1:
                        last_member = member[-1]
                        member = member[:-1]
                        last_member = last_member + "]"
                        member.append(last_member)
                        one_IntegerLiteral = 0
                else:
                    #
                    if select_operator == 3:

                        select_operator = 2
                    elif select_operator == 2:
                        # last_member = member[-1]
                        # member = member[:-1]
                        # member.append("(" + last_member)
                        operator.append("?")
                        select_operator = 1
                    elif select_operator ==1:
                        # last_member = member[-1]
                        # member = member[:-1]
                        # member.append(last_member + ")")
                        operator.append(":")
                        select_operator=0
                    #
                    member.append(regx_MemberExpr_obj.group(1))
                    joint_sign = joint_sign - 1

            if ternary_sign == 3:
                member3.append(regx_MemberExpr_obj.group(1))
            elif ternary_sign == 4:
                member4.append(regx_MemberExpr_obj.group(1))
            elif ternary_sign == 5:
                member5.append(regx_MemberExpr_obj.group(1))

        elif regx_RecoveryExpr.search(line):
            num_contains=1

        elif regx_IntegerLiteral.search(line):
            regx_IntegerLiteral_obj = regx_IntegerLiteral.search(line)
            if ternary_sign == 3:
                if one_sign == 1:
                    member3_1 = member3[-1]
                    member3.pop()
                    member3_1 = member3_1 + "[%s]" % regx_IntegerLiteral_obj.group(1)
                    member3.append(member3_1)
                    # print("__________memnber3", member3)
                    one_sign = 0
                else:
                    if two_sign == 2:
                        member3_1 = member3[-1]
                        member3.pop()
                        member3_1 = member3_1 + "[%s:" % regx_IntegerLiteral_obj.group(1)
                        member3.append(member3_1)
                        two_sign = 1
                    elif two_sign == 1:
                        member3_1 = member3[-1]
                        member3.pop()
                        member3_1 = member3_1 + "%s]" % regx_IntegerLiteral_obj.group(1)
                        member3.append(member3_1)
                        two_sign = 0
                    else:
                        member3.append(regx_IntegerLiteral_obj.group(1))
                    # print("__________memnber3", member3)




            elif ternary_sign == 4:
                if one_sign == 1:
                    member4_1 = member4[-1]
                    member4.pop()
                    member4_1 = member4_1 + "[%s]" % regx_IntegerLiteral_obj.group(1)
                    member4.append(member4_1)
                    # print("__________memnber4", member4)
                    one_sign = 0
                else:
                    if two_sign == 2:
                        member4_1 = member4[-1]
                        member4.pop()
                        member4_1 = member4_1 + "[%s:" % regx_IntegerLiteral_obj.group(1)
                        member4.append(member4_1)
                        two_sign = 1
                    elif two_sign == 1:
                        member4_1 = member4[-1]
                        member4.pop()
                        member4_1 = member4_1 + "%s]" % regx_IntegerLiteral_obj.group(1)
                        member4.append(member4_1)
                        two_sign = 0
                    else:
                        member4.append(regx_IntegerLiteral_obj.group(1))
                    # print("__________memnber4", member4)

            elif ternary_sign == 5:
                if one_sign == 1:
                    member5_1 = member5[-1]
                    member5.pop()
                    member5_1 = member5_1 + "[%s]" % regx_IntegerLiteral_obj.group(1)
                    member5.append(member5_1)
                    # print("__________memnber5", member5)
                    one_sign = 0
                else:
                    if two_sign == 2:
                        member5_1 = member5[-1]
                        member5.pop()
                        member5_1 = member5_1 + "[%s:" % regx_IntegerLiteral_obj.group(1)
                        member5.append(member5_1)
                        two_sign = 1

                    elif two_sign == 1:
                        member5_1 = member5[-1]
                        member5.pop()
                        member5_1 = member5_1 + "%s]" % regx_IntegerLiteral_obj.group(1)
                        member5.append(member5_1)
                        two_sign = 0
                    else:
                        member5.append(regx_IntegerLiteral_obj.group(1))
            else:
                if two_sign==2:
                    member_last=member[-1]
                    member.pop()
                    member_last=member_last+"[%s:" % regx_IntegerLiteral_obj.group(1)
                    member.append(member_last)
                    two_sign=1
                elif two_sign==1:
                    member_last=member[-1]
                    member.pop()
                    member_last=member_last+"%s]" % regx_IntegerLiteral_obj.group(1)
                    member.append(member_last)
                    two_sign=0
                else:
                    if case_sign1==1:
                        pass
                    else:
                        if judge_num!=1 and judge_num!=2 and judge_num!=3:
                        # if ((judge_num!=3) or (judge_num!=4) or (judge_num!=5)):
                            member.append(regx_IntegerLiteral_obj.group(1))

            if pp==1:
                pp=0
                continue
            regx_IntegerLiteral_obj = regx_IntegerLiteral.search(line)
            if if_sign==1:
                if judge_num==1:
                    last_member = member[-1]
                    member = member[:-1]
                    last_member = last_member + "==" + regx_IntegerLiteral_obj.group(1)
                    member.append(last_member)
                    last_member = ""
                    judge_num=0
                elif judge_num==2:
                    last_member = member[-1]
                    member = member[:-1]
                    last_member = last_member + "<" + regx_IntegerLiteral_obj.group(1)
                    member.append(last_member)
                    last_member = ""
                    judge_num = 0
                elif judge_num==3:
                    last_member = member[-1]
                    member = member[:-1]
                    last_member = last_member + ">" + regx_IntegerLiteral_obj.group(1)
                    member.append(last_member)
                    last_member = ""
                    judge_num = 0
            elif case_sign==1:
                content_case=regx_IntegerLiteral_obj.group(1)+":"
                always_content = always_content + case_space*" "+content_case + "\n"
                content_case=""
                case_sign=0
            elif for_sign==1:
                member.append(regx_IntegerLiteral_obj.group(1))
                operator.append(";")
                for i in range(len(operator)):
                    member.insert(merge_operator, operator[i])
                    merge_operator = merge_operator + 2
                for i in range(len(member)):
                    finish_content = finish_content + member[i]
                operator = []
                member = []
                IntegerLiteral = []
                one_IntegerLiteral = 0
                merge_operator = 1
                last_member = ""
                new_member = ""

            else:
                regx_IntegerLiteral_obj = regx_IntegerLiteral.search(line)

                ##针对二元判断操作符进行处理 ?A:B
                if operator_first == ">" or operator_first == "<" or operator_first=="==" or operator_first==">=" or operator_first=="<=" or operator_first=="!=":
                    last_member = member[-1]
                    member = member[:-1]
                    last_member = "(" + last_member + operator_first + regx_IntegerLiteral_obj.group(1) + ")"
                    member.append(last_member)
                    operator_first = ""
                    joint_sign = -1
                    judge_colon = 1  ##二元判断符后面冒号的标记位
                ##正常处理带位宽的信号A[num：num]
                elif num_contains==1:
                    last_member = member[-1]
                    member = member[:-1]
                    if one_IntegerLiteral == 0:
                        last_member = last_member + "[" + regx_IntegerLiteral_obj.group(1)
                        member.append(last_member)
                        one_IntegerLiteral = 1
                    else:
                        last_member = last_member + ":" + regx_IntegerLiteral_obj.group(1) + "]"
                        member.append(last_member)
                        one_IntegerLiteral = 0
                        num_contains=0
                else:
                    if select_operator==2:
                        operator.append("?")
                        member.append(regx_IntegerLiteral_obj.group(1))
                        select_operator=1
                        continue
                    elif select_operator==1:
                        operator.append(":")
                        member.append(regx_IntegerLiteral_obj.group(1))
                        select_operator=0
                        continue
                    # member.append(regx_IntegerLiteral_obj.group(1))
                    # operator.append(";")
                    if ternary_sign==0:
                        pass
                        # end_output_always()
                    else:
                        # always_content = always_content + recent_space * " " + finish_content + "\n"
                        pass

                        operator = []
                        member = []
                        IntegerLiteral = []
                        one_IntegerLiteral = 0
                        merge_operator = 1
                        finish_content = ""
                        last_member = ""
                        new_member = ""





        elif regx_BreakStmt.search(line):
            operator.append(";")
            end_output_always()
            regx_BreakStmt_obj=regx_BreakStmt.search(line)

            while 1:
                if always_function==1:
                    if case_sign1 == 0 and len(regx_BreakStmt_obj.group(1)) <= begin_end[-1]:
                        always_content = always_content + begin_end[-1] * " " + "end\n"
                        if begin_end[-1] == endcase_space and endcase_sign == 1:
                            always_content = always_content + "\n" + endcase_space * " " + "endcase\n"
                            endcase_sign = 0
                        begin_end.pop()
                    elif case_sign1 == 0 and len(regx_BreakStmt_obj.group(1)) <= begin_end[-1] + 2:
                        always_content = always_content + begin_end[-1] * " " + "end\n"
                        if begin_end[-1] == endcase_space and endcase_sign == 1:
                            always_content = always_content + "\n" + endcase_space * " " + "endcase\n"
                            endcase_sign = 0
                        begin_end.pop()
                    elif case_sign1 == 0 and len(regx_BreakStmt_obj.group(1)) <= begin_end[-1] + 4:
                        always_content = always_content + begin_end[-1] * " " + "end\n"
                        if begin_end[-1] == endcase_space and endcase_sign == 1:
                            always_content = always_content + "\n" + endcase_space * " " + "endcase\n"
                            endcase_sign = 0
                        begin_end.pop()
                    else:
                        always_content = always_content + "\n"

                        break
                    if len(begin_end)==0:
                        always_content = always_content + "\n"
                        break

                else:
                    if case_sign1==0 and len(regx_BreakStmt_obj.group(1)) <= begin_end[-1]:
                        always_content=always_content+begin_end[-1]*" "+ "end\n"
                        if begin_end[-1]==endcase_space and endcase_sign==1:
                            always_content=always_content+"\n"+endcase_space*" "+ "endcase\n"
                            endcase_sign=0
                        begin_end.pop()
                    elif case_sign1==0 and len(regx_BreakStmt_obj.group(1)) <= begin_end[-1]+2:
                        always_content = always_content + begin_end[-1] * " " + "end\n"
                        if begin_end[-1] == endcase_space and endcase_sign == 1:
                            always_content = always_content + "\n" + endcase_space * " " + "endcase\n"
                            endcase_sign = 0
                        begin_end.pop()
# 修改case缺失end部分
                    elif case_sign1==0 and len(regx_BreakStmt_obj.group(1)) <= begin_end[-1]+4:
                        always_content = always_content + begin_end[-1] * " " + "end\n"
                        if begin_end[-1] == endcase_space and endcase_sign == 1:
                            always_content = always_content + "\n" + endcase_space * " " + "endcase\n"
                            endcase_sign = 0
                        begin_end.pop()

 #
                    else:
                        always_content = always_content + "\n"
                        break
                    if len(begin_end) == 0:
                        always_content = always_content + "\n"
                        break

        elif regx_DefaultStmt.search(line):
            case_sign=0
            case_sign1=0
            endcase_sign=1
            always_content = always_content + recent_space * " " + "default:\n"
            always_content = always_content + (recent_space) * " " + "begin\n"
            begin_end.append(recent_space)
            endcase_space=recent_space

        elif regx_none.fullmatch(line):
            operator.append(";")
            end_output_always()
            if begin_end:
                for i in range(len(begin_end)):
                    always_content = always_content + begin_end[-1] * " " + "end\n"
                    if begin_end[-1]==endcase_space and endcase_sign==1:
                        always_content=always_content+"\n"+endcase_space*" "+ "endcase\n"
                        endcase_sign=0
                    begin_end.pop()
            if always_combilogic==1:
                always.insert(0,always_tir)
            always_combilogic=0
            always_function=0
            returnstmt_sign=0
            ternary_sign=0



        elif regx_ReturnStmt.search(line):
            returnstmt_sign=1

        elif regx_Dumping_always.search(line):
            end_output_always()
            regx_Dumping_always_obj = regx_Dumping_always.search(line)
            always_content = always_content  + "end\n"
            print(regx_Dumping_always_obj.group(1))
            if always_block_num<len(always):
                always_content=always_content+always[always_block_num]+"\n"
                # always_content =  always[always_block_num] + "\n"+always_content
                always_block_num=always_block_num+1
            always_content = always_content + "begin\n"
            has_else = 0
            else_space = []
            begin_end = []
            recent_space = 0



        continue








    # if ConditionalOperator_sign==2:
    #     if regx_BinaryOperator.search(line):
    #         regx_BinaryOperator_obj=regx_BinaryOperator.search(line)
    #         operator1.append(regx_BinaryOperator_obj.group(2))
    #     elif regx_MemberExpr.search(line):
    #         regx_MemberExpr_obj=regx_MemberExpr.search(line)
    #         member1.append(regx_MemberExpr_obj.group(1))
    #     elif regx_IntegerLiteral.search(line):
    #         regx_IntegerLiteral_obj=regx_IntegerLiteral.search(line)
    #         member1.append(regx_IntegerLiteral_obj.group(1))



    ##获取模块名称
    if regx_Dumping.fullmatch(line):
        regx_Dumping_obj=regx_Dumping.fullmatch(line)
        module_name=regx_Dumping_obj.group(1)
        regx_Dumping_assign = re.compile("Dumping %s::assign_(\w+)" % module_name)
        regx_Dumping_function= re.compile("Dumping %s::function_(\w+)" % module_name)
        assign_sign=1
        regx_Dumping_always =re.compile("Dumping %s::always_block(\d*)" % module_name)
        regx_Dumping_always_combigolic=re.compile("Dumping %s::always_combilogic_block(\d*)" % module_name)
        # print(regx_Dumping_always)
    ##处理信号定义部分
    elif regx_FieldDecl.search(line):
        regx_FieldDecl_obj=regx_FieldDecl.search(line)
        if "line" in regx_FieldDecl_obj.group(1):
            new_line_iden=1
            ##默认端口为wire，信号为reg
            if "sc_inout<" in regx_FieldDecl_obj.group(3):
                FieldDecl_cont = FieldDecl_cont + "inout wire "
                module_port = module_port + "%s , " % regx_FieldDecl_obj.group(2)
            elif "sc_in_clk" in regx_FieldDecl_obj.group(3):
                FieldDecl_cont=FieldDecl_cont+"input wire "
                module_port=module_port+"%s , "%regx_FieldDecl_obj.group(2)
            elif "sc_in<" in regx_FieldDecl_obj.group(3):
                FieldDecl_cont=FieldDecl_cont+"input wire "
                module_port=module_port+"%s , "%regx_FieldDecl_obj.group(2)
            elif "sc_out<" in regx_FieldDecl_obj.group(3):
                FieldDecl_cont=FieldDecl_cont+"output wire "
                module_port = module_port + "%s , " % regx_FieldDecl_obj.group(2)
            elif "sc_signal" in regx_FieldDecl_obj.group(3):
                if "func_" in regx_FieldDecl_obj.group(2):
                    function_signal=regx_FieldDecl_obj.group(2)[5:]
                    if regx_FieldDecl_num.search(regx_FieldDecl_obj.group(3)):
                        function_signal_width = int(regx_FieldDecl_obj_num.group(0)) - 1
                    continue
                FieldDecl_cont=FieldDecl_cont+"wire "
                finish_write_port=1
            elif "sc_uint<" in regx_FieldDecl_obj.group(3):
                FieldDecl_cont = FieldDecl_cont + "wire "
            elif "sc_int<" in regx_FieldDecl_obj.group(3):
                FieldDecl_cont = FieldDecl_cont + "wire "
            elif "sc_biguint<" in regx_FieldDecl_obj.group(3):
                FieldDecl_cont = FieldDecl_cont + "wire "
            elif "sc_bigint<" in regx_FieldDecl_obj.group(3):
                FieldDecl_cont = FieldDecl_cont + "wire "
            elif "sc_uint<" in regx_FieldDecl_obj.group(3):
                FieldDecl_cont = FieldDecl_cont + "wire "
            elif "sc_int<" in regx_FieldDecl_obj.group(3):
                FieldDecl_cont = FieldDecl_cont + "wire "
            elif "sc_logic<" in regx_FieldDecl_obj.group(3):
                FieldDecl_cont = FieldDecl_cont + "wire "
            elif "sc_bit<" in regx_FieldDecl_obj.group(3):
                FieldDecl_cont = FieldDecl_cont + "wire "
            else:
                instantiation_modules.append( regx_FieldDecl_obj.group(3)+" "+regx_FieldDecl_obj.group(2))
                continue

            if regx_FieldDecl_num.search(regx_FieldDecl_obj.group(3)):
                regx_FieldDecl_obj_num=regx_FieldDecl_num.search(regx_FieldDecl_obj.group(3))
                regx_FieldDecl_obj_num1=int(regx_FieldDecl_obj_num.group(0))-1
                if regx_FieldDecl_obj_num1==0:
                    FieldDecl_cont = FieldDecl_cont + " "
                else:
                    FieldDecl_cont = FieldDecl_cont + "[%s:0] "%regx_FieldDecl_obj_num1
            FieldDecl_cont=FieldDecl_cont+"%s"%regx_FieldDecl_obj.group(2)+";\n"
        else:
            if ";" in FieldDecl_cont:
                FieldDecl_cont=FieldDecl_cont[:-2]
            FieldDecl_cont=FieldDecl_cont+",%s"%regx_FieldDecl_obj.group(2)+";\n"
            if finish_write_port==0:
                module_port = module_port + "%s , " % regx_FieldDecl_obj.group(2)
            elif finish_write_port==1:
                # module_port = module_port[:-2]
                finish_write_port=2

    elif regx_VarDecl.search(line):
        regx_VarDecl_obj=regx_VarDecl.search(line)
        if len(instantiation_content):
            instantiation_content=instantiation_content[:-2]
            instantiation_content = instantiation_content +  "\n);\n"
        instantiation_content=instantiation_content+regx_VarDecl_obj.group(2)+" "+regx_VarDecl_obj.group(1)+"\n(\n"

    # elif regx_Finish_FieldDecl.search(line):
    #     for i in range(len(instantiation_modules)):
    #         names["instantiation_"+str(instantiation_modules[i])]=""



    elif regx_MemberExpr1.search(line):
        regx_MemberExpr1_obj=regx_MemberExpr1.search(line)
        # instantiation_content=instantiation_content+regx_MemberExpr1_obj.group(1)
        instantiation_first=regx_MemberExpr1_obj.group(1)
        instantiation=2

    elif regx_MemberExpr2.search(line):
        range_sign=1
        two_sign=2



    ##assign开头部分
    elif assign_sign==1 and regx_Dumping_assign.match(line):
        regx_Dumping_assign_obj=regx_Dumping_assign.match(line)
        Lvalue=regx_Dumping_assign_obj.group(1)
        finish_content="assign "+finish_content+"%s="%Lvalue
        assign_first=1

        if len(instantiation_content):
            instantiation_content = instantiation_content[:-2]
            instantiation_content = instantiation_content + "\n);\n"

    ##结尾写入部分
    elif regx_none.fullmatch(line):
        if one_IntegerLiteral==1:
            last_member = member[-1]
            member = member[:-1]
            last_member=last_member+"]"
            member.append(last_member)
            one_IntegerLiteral =0

        if ternary_sign == 5:
            print("3",member3,operator3)
            print("4",member4,operator4)
            print("5",member5,operator5)
            ternary_content = finish_content+ternary_content + ternary_joint(member3, operator3) + "?"+ternary_joint(member4,operator4)+":"+ternary_joint(member5,operator5)+";"
            print("ternary_content:          ",ternary_content)

        ##对assign部分的位选取操作进行处理
        for i in range(len(member)):
            if "var_" in member[i]:
                member=member[2:-2]
                var_member.append(member[i])

                ##删去中间变量前缀
                finish_content="assign %s="%member[0][4:]

                break



        if member:
            # operator.append(";")
            if len(member)>1:
                joint()
            member.append(" ;")
            member=member[1:]
            for i in range(len(operator)):
                member.insert(merge_operator,operator[i])
                merge_operator = merge_operator + 2
            print(member)
            for i in range(len(member)):
                finish_content=finish_content+member[i]
        else:
            print("member none")
        # finish_content=finish_content+";"
        print(finish_content)
        if ternary_sign==5:
            assign_content=assign_content+ternary_content+"\n"
        else:
            assign_content=assign_content+finish_content+"\n"






        Lvalue = ""
        operator = []
        member = []
        IntegerLiteral = []
        one_IntegerLiteral = 0
        merge_operator = 1
        finish_content = ""
        always_sign=0
        last_member=""
        new_member=""
        bracket_sign=0
        ConditionalOperator_sign=0
        ternary_sign=0
        member3=[]
        member4=[]
        member5=[]
        operator3=[]
        operator4=[]
        operator5=[]
        len_ternary=0
        len_member=0
        ternary_content = ""
        two_sign=0




    ##识别到括号标识符，进行合并操作和给出合并标志位joint_sign，该标志位以A[num：num]为常规情况，A[num]和?A:B为特殊情况
    elif regx_ParenExpr.search(line):
        if one_IntegerLiteral==1:
            last_member = member[-1]
            member = member[:-1]
            last_member=last_member+"]"
            member.append(last_member)
            one_IntegerLiteral =0

        joint()
        joint_sign=2
        bracket_sign=1

    elif regx_CXXOperatorCallExpr4.search(line):
        print("++++++++++++")
        one_sign=1


    elif regx_CXXOperatorCallExpr.search(line):
        regx_CXXOperatorCallExpr_obj=regx_CXXOperatorCallExpr.search(line)
        # joint()
        if one_IntegerLiteral==1:
            last_member = member[-1]
            member = member[:-1]
            last_member=last_member+"]"
            member.append(last_member)
            one_IntegerLiteral =0

        if regx_CXXOperatorCallExpr_obj.group(1)==","or regx_CXXOperatorCallExpr_obj.group(1)=="&":
            operator_first=regx_CXXOperatorCallExpr_obj.group(1)
        else:
            operator.append(regx_CXXOperatorCallExpr_obj.group(1))

    elif regx_ConditionalOperator.search(line):
        regx_ConditionalOperator_obj=regx_ConditionalOperator.search(line)
        select_operator=3
        ConditionalOperator_sign=1
        ternary_sign=3
        len_ternary=len(regx_ConditionalOperator_obj.group(1))

    elif regx_CXXBindTemporaryExpr.search(line):
        regx_CXXBindTemporaryExpr_obj=regx_CXXBindTemporaryExpr.search(line)
        if len(regx_CXXBindTemporaryExpr_obj.group(1))==(len_ternary+2) :
            if ternary_sign==3:
                ternary_sign=4
            elif ternary_sign==4:
                ternary_sign=5




    elif regx_ImplicitCastExpr.search(line):
        ImplicitCastExpr_sign=2


    elif regx_BinaryOperator.search(line):
        regx_BinaryOperator_obj=regx_BinaryOperator.search(line)

        if one_IntegerLiteral==1:
            last_member = member[-1]
            member = member[:-1]
            last_member=last_member+"]"
            member.append(last_member)
            one_IntegerLiteral =0

        if joint_sign==2:
            # if regx_BinaryOperator_obj.group(2)!=",":
            #     operator.append(regx_BinaryOperator_obj.group(2))
            # else:
            #     operator_first = regx_BinaryOperator_obj.group(2)
            operator_first = regx_BinaryOperator_obj.group(2)
        else:
            operator.append(regx_BinaryOperator_obj.group(2))

        if ternary_sign==3:
            operator3.append(regx_BinaryOperator_obj.group(2))
        elif ternary_sign==4:
            operator4.append(regx_BinaryOperator_obj.group(2))
        elif ternary_sign==5:
            operator5.append(regx_BinaryOperator_obj.group(2))

    elif regx_UnaryOperator.search(line):
        regx_UnaryOperator_obj=regx_UnaryOperator.search(line)
        sign_fist=regx_UnaryOperator_obj.group(1)


    elif regx_MemberExpr.search(line):
        member_sign=2
        if len(member) > 1:
            joint()
        regx_MemberExpr_obj = regx_MemberExpr.search(line)

        if instantiation==1:
            instantiation=0

            instantiation_content=instantiation_content+instantiation_first+"("+regx_MemberExpr_obj.group(1)+") ,\n"
            continue
        elif instantiation==2:
            if recent_instantiation!=regx_MemberExpr_obj.group(1):
                if len(recent_instantiation):
                    instantiation_content=instantiation_content[:-2]
                    instantiation_content=instantiation_content+("\n);\n")
                    instantiation_content = instantiation_content + "\n"+instantiation_modules[instantiation_num]+"\n(\n"
                    instantiation_num=instantiation_num+1
                else:
                    instantiation_content = instantiation_content + instantiation_modules[instantiation_num] + "\n(\n"
                    instantiation_num = instantiation_num + 1
            recent_instantiation=regx_MemberExpr_obj.group(1)
            instantiation = 1
            continue
        if assign_first==1:
            wire_sign.append(regx_MemberExpr_obj.group(1))
            assign_first=2
        if sign_fist:
            new_member=sign_fist+regx_MemberExpr_obj.group(1)
            sign_fist=""
        else:
            new_member=regx_MemberExpr_obj.group(1)

        if if_sign==1:
            content_if=content_if+"{"+new_member
        else:

            if select_operator==3:
                select_operator=2
            elif select_operator==2:
                last_member = member[-1]
                member = member[:-1]
                last_member=last_member+" ? "
                member.append(last_member)
                select_operator=1


            ##处理函数的包含关系
            if "function" in regx_MemberExpr_obj.group(1):
                new_member = regx_MemberExpr_obj.group(1) + "("
            elif len(member) and ("function" in member[-1]):
                new_member = "func_"+member[-1][9:]+regx_MemberExpr_obj.group(1) + ")"
                member.pop()
            member.append(new_member)



            if one_IntegerLiteral==1:
                last_member = member[-1]
                member = member[:-1]
                last_member=last_member+"]"
                member.append(last_member)
                one_IntegerLiteral =0

            ##为二元判断符”？“输出”：“
            # if judge_colon==1:
            #     member.append(":")
            #     judge_colon=0
            joint_sign = joint_sign - 1

            ##为二元判断符”？“输出”：“
            if select_operator==1:
                member.append(":")
                select_operator=0


        if ternary_sign==3:
            member3.append(regx_MemberExpr_obj.group(1))
        elif ternary_sign==4:
            member4.append(regx_MemberExpr_obj.group(1))
        elif ternary_sign==5:
            member5.append(regx_MemberExpr_obj.group(1))





    elif regx_IntegerLiteral.search(line):
        regx_IntegerLiteral_obj = regx_IntegerLiteral.search(line)


        if ternary_sign==3:
            if one_sign == 1:
                member3_1 = member3[-1]
                member3.pop()
                member3_1 = member3_1 + "[%s]" % regx_IntegerLiteral_obj.group(1)
                member3.append(member3_1)
                # print("__________memnber3", member3)
                one_sign = 0
            else:
                if two_sign == 2:
                    member3_1 = member3[-1]
                    member3.pop()
                    member3_1=member3_1+"[%s:"%regx_IntegerLiteral_obj.group(1)
                    member3.append(member3_1)
                    two_sign=1
                elif two_sign==1:
                    member3_1 = member3[-1]
                    member3.pop()
                    member3_1=member3_1+"%s]"%regx_IntegerLiteral_obj.group(1)
                    member3.append(member3_1)
                    two_sign=0
                else:
                    member3.append(regx_IntegerLiteral_obj.group(1))
                # print("__________memnber3", member3)




        elif ternary_sign==4:
            if one_sign == 1:
                member4_1 = member4[-1]
                member4.pop()
                member4_1 = member4_1 + "[%s]" % regx_IntegerLiteral_obj.group(1)
                member4.append(member4_1)
                # print("__________memnber4", member4)
                one_sign = 0
            else:
                if two_sign == 2:
                    member4_1 = member4[-1]
                    member4.pop()
                    member4_1 = member4_1 + "[%s:" % regx_IntegerLiteral_obj.group(1)
                    member4.append(member4_1)
                    two_sign = 1
                elif two_sign == 1:
                    member4_1 = member4[-1]
                    member4.pop()
                    member4_1 = member4_1 + "%s]" % regx_IntegerLiteral_obj.group(1)
                    member4.append(member4_1)
                    two_sign = 0
                else:
                    member4.append(regx_IntegerLiteral_obj.group(1))
                # print("__________memnber4", member4)

        elif ternary_sign==5:
            if one_sign == 1:
                member5_1 = member5[-1]
                member5.pop()
                member5_1 = member5_1 + "[%s]" % regx_IntegerLiteral_obj.group(1)
                member5.append(member5_1)
                # print("__________memnber5", member5)
                one_sign = 0
            else:
                if two_sign == 2:
                    member5_1 = member5[-1]
                    member5.pop()
                    member5_1 = member5_1 + "[%s:" % regx_IntegerLiteral_obj.group(1)
                    member5.append(member5_1)
                    two_sign = 1

                elif two_sign == 1:
                    member5_1 = member5[-1]
                    member5.pop()
                    member5_1 = member5_1 + "%s]" % regx_IntegerLiteral_obj.group(1)
                    member5.append(member5_1)
                    two_sign = 0
                else:
                    member5.append(regx_IntegerLiteral_obj.group(1))
                # print("__________memnber5", member5)


        if ImplicitCastExpr_sign==1:
            if operator_first==">" or operator_first=="<" or operator_first=="==" or operator_first==">=" or operator_first=="<=" or operator_first=="!=":
                last_member=member[-1]
                member=member[:-1]
                last_member="("+last_member+operator_first+regx_IntegerLiteral_obj.group(1)+")"
                member.append(last_member)
                operator_first=""
            else:
                last_member = regx_IntegerLiteral_obj.group(1)
                member.append(last_member)
            continue







        #以member_sign为标记，如果MemberExpr后面接着IntegerLiteral就作A[num：num]处理，否则作为对象加入member。
        if member_sign==1:
            member_sign=2
            last_member = member[-1]
            member = member[:-1]

            ##针对二元判断操作符进行处理 ?A:B
            if operator_first == ">" or operator_first == "<" or operator_first=="==" or operator_first==">=" or operator_first=="<=" or operator_first=="!=":
                last_member = "(" + last_member + operator_first + regx_IntegerLiteral_obj.group(1) + ")"
                member.append(last_member)
                operator_first = ""
                joint_sign = -1
                judge_colon = 1  ##二元判断符后面冒号的标记位
            ##正常处理带位宽的信号A[num：num]
            else:
                if one_IntegerLiteral == 0:
                    last_member = last_member + "[" + regx_IntegerLiteral_obj.group(1)
                    member.append(last_member)
                    one_IntegerLiteral = 1
                else:
                    last_member = last_member + ":" + regx_IntegerLiteral_obj.group(1) + "]"
                    member.append(last_member)
                    one_IntegerLiteral = 0

            ##第二种情况是IntegerLiteral里面的数字作为member，A=A+1。
        else:
            if select_operator == 3:
                select_operator = 2
            elif select_operator == 2:
                last_member = member[-1]
                member = member[:-1]
                last_member = last_member + " ? "
                member.append(last_member)
                select_operator = 1

            last_member = regx_IntegerLiteral_obj.group(1)
            member.append(last_member)

            ##为二元判断符”？“输出”：“
            if select_operator == 1:
                member.append(":")
                select_operator = 0













        # ##第一种情况是IntegerLiteral里面的数字作为位宽的情况A[num：num]
        # if bracket_sign==1:
        #     last_member = member[-1]
        #     member = member[:-1]
        #
        #     ##针对二元判断操作符进行处理 ?A:B
        #     if operator_first==">"or operator_first=="<":
        #         last_member="("+last_member+operator_first+regx_IntegerLiteral_obj.group(1)+")"
        #         member.append(last_member)
        #         operator_first=""
        #         joint_sign=-1
        #         judge_colon=1  ##二元判断符后面冒号的标记位
        #     ##正常处理带位宽的信号A[num：num]
        #     else:
        #         if one_IntegerLiteral==0:
        #             last_member=last_member+"["+regx_IntegerLiteral_obj.group(1)
        #             member.append(last_member)
        #             one_IntegerLiteral=1
        #         else:
        #             last_member = last_member +  ":"+regx_IntegerLiteral_obj.group(1) + "]"
        #             member.append(last_member)
        #             one_IntegerLiteral = 0
        # ##第二种情况是IntegerLiteral里面的数字作为member，A=A+1。
        # else:
        #     if select_operator==3:
        #         select_operator=2
        #     elif select_operator==2:
        #         last_member = member[-1]
        #         member = member[:-1]
        #         last_member=last_member+" ? "
        #         member.append(last_member)
        #         select_operator=1
        #
        #     last_member = regx_IntegerLiteral_obj.group(1)
        #     member.append(last_member)
        #
        #     ##为二元判断符”？“输出”：“
        #     if select_operator==1:
        #         member.append(":")
        #         select_operator=0




    ##always触发信号处理（边沿触发）
    elif regx_sensitive.match(line):

        regx_sensitive = re.compile("sensitive: (.*);(.*)")
        if regx_sensitive.match(line):
            regx_sensitive_obj = regx_sensitive.match(line)
            pos = regx_sensitive_obj.group(1)
            neg = regx_sensitive_obj.group(2)
            ##always触发条件部分
            always_tir = "\nalways @("

            if pos:
                pos1 = pos.split(",")
            else:
                pos1 = []
            if neg:
                neg1 = neg.split(",")
            else:
                neg1 = []


            if len(pos1):
                for i in range(len(pos1)):
                    # print(i)
                    always_tir = always_tir + " posedge " + pos1[i]
                    if i != (len(pos1) - 1):
                        always_tir = always_tir + " or "
                if len(neg1):
                    always_tir = always_tir + " or "
                    for i in range(len(neg1)):
                        always_tir = always_tir + " negedge " + neg1[i]
                        if i != (len(neg1) - 1):
                            always_tir = always_tir + " or "

                    always_tir = always_tir + ")"
                else:
                    always_tir = always_tir + ")"
            else:
                if len(neg1):
                    for i in range(len(neg1)):
                        always_tir = always_tir + " negedge " + neg1[i]
                        if i != (len(neg1) - 1):
                            always_tir = always_tir + " or "

                    always_tir = always_tir + ")"
                # print(always_tir)
            always.append(always_tir)

    ##always开头部分
    elif regx_Dumping_always.search(line):
        end_output_always()
        regx_Dumping_always_obj=regx_Dumping_always.search(line)
        print(regx_Dumping_always_obj.group(1))
        always_sign=1
        always_output_sign=1
        always_firstport=1

    elif regx_Dumping_always_combigolic.search(line):
        end_output_always()
        regx_Dumping_always_obj = regx_Dumping_always.search(line)
        # print(regx_Dumping_always_obj.group(1))
        always_sign = 1
        always_output_sign = 1
        always_combilogic=1
        always_tir="\nalways @( * )"

    elif regx_Dumping_function.search(line):
        end_output_always()
        regx_Dumping_function_obj = regx_Dumping_function.search(line)
        # print(regx_Dumping_always_obj.group(1))
        always_sign = 1
        always_output_sign = 1
        always_function=1

        always_tir="\nfunction %s"%("func_"+regx_Dumping_function_obj.group(1))




for line in FieldDecl_cont.split("\n"):
    ##对assign左值的信号进行reg转化
    if regx_wire.match(line):
        regx_wire_obj=regx_wire.match(line)
        if regx_wire_obj.group(1) in reg_sign:
            line=re.sub("wire","reg",line)
            if regx_wire_obj.group(1) in wire_sign:
                print("\033[1;31m error:Assign conflict \033[0m")
                ###### sys.exit(1)
    ##always左值的信号更改其端口值为reg
    elif regx_io_reg.match(line):
        regx_io_reg_obj = regx_io_reg.match(line)
        if regx_io_reg_obj.group(2) in reg_sign:
            line = re.sub("wire", "reg", line)
            if regx_io_reg_obj.group(2) in wire_sign:
                print("\033[1;31m error:Assign conflict \033[0m")
                ####### sys.exit(1)
    FieldDecl_cont_new=FieldDecl_cont_new+line+"\n"


##结尾处理16进制转换问题
for line in always_content.split("\n"):
    if regx_IntegerLiteral2.search(line):
        regx_IntegerLiteral2_obj = regx_IntegerLiteral2.search(line)
        bit = 4 * len(regx_IntegerLiteral2_obj.group(1))
        line=re.sub(regx_IntegerLiteral2,"="+str(bit) + "'h" + regx_IntegerLiteral2_obj.group(1),line)
        # re.sub(regx_IntegerLiteral2,"00000", line)
        new_always_content=new_always_content+line+"\n"
    else:
        new_always_content = new_always_content + line + "\n"
    # if regx_var.search(line):
    #     regx_var_obj=regx_var.search(line)
    #     var_member.append(regx_var_obj.group(1))

##处理SystemC用来在always中进行位选操作的中间变量（var_xxx）
for i in range(len(reg_sign)):
    if regx_var.match(reg_sign[i]):
        regx_var_obj=regx_var.match(reg_sign[i])
        var_member.append(reg_sign[i])
        new_always_content=re.sub("%s<=%s;"%(reg_sign[i],regx_var_obj.group(1)),"",new_always_content)
        new_always_content = re.sub("%s<=%s;" % (regx_var_obj.group(1),reg_sign[i]), "", new_always_content)
        new_always_content=re.sub("%s"%reg_sign[i],"%s"%regx_var_obj.group(1),new_always_content)
        FieldDecl_cont_new=re.sub("reg.*%s;"%reg_sign[i],"",FieldDecl_cont_new)
for i in range(len(wire_sign)):
    if regx_var.match(wire_sign[i]):
        regx_var_obj = regx_var.match(wire_sign[i])
        var_member.append(wire_sign[i])
        FieldDecl_cont_new = re.sub("wire.*%s;" % wire_sign[i], "", FieldDecl_cont_new)
        # assign_content=re.sub("var_","",assign_content)

##生成verilog
new_ast_code.write("module "+module_name+ " ( "+module_port[0:-2]+ ");\n")
new_ast_code.write(FieldDecl_cont_new)
new_ast_code.write(instantiation_content)
new_ast_code.write(assign_content)
print(module_port,"+++")
print(FieldDecl_cont_new)
print(instantiation_content)
print(assign_content)
# print(var_member)
##对多个内容为空的case的处理
new_always_content=re.sub(regx_conti_colon,",",new_always_content)



# print(new_always_content)



if "function" in always_tir:
    new_always_content = always_tir + "\n" + "begin\n" + new_always_content + "end\n" + "endfunction\n"
else :
    new_always_content=always[0]+"\n"+"begin\n"+new_always_content+"end\n"
if always_output_sign==1:
    new_ast_code.write(new_always_content)





print("_______________\n",new_always_content)
print("++++++++++++++\n",always)
new_ast_code.write("endmodule\n")
print(wire_sign)
print(reg_sign)
print(instantiation_modules)
