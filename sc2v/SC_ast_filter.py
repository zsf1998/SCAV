import re
import sys
SCast_file = sys.argv[1]

# SCast_file = "sm3_control.txt"
# SCast_file = "messagecompress.txt"
# SCast_file = "test.txt"
# SCast_file = "func_test.txt"
#SCast_file = "Ternary_operator.txt"
# SCast_file = "2.txt"

f_ast= open(SCast_file, 'r')
txt=f_ast.read()
new_ast_code  = open(SCast_file[:-4]+"_new.txt", 'a+')
# new_ast_code  = open(SCast_file[:-4]+"_new1.txt", 'a+')
new_ast_code.truncate(0)
regx_ImplicitCastExpr=re.compile("ImplicitCastExpr")
regx_CXXMemberCallExpr=re.compile("CXXMemberCallExpr")
regx_CXXThisExpr=re.compile("CXXThisExpr")
regx_DeclRefExpr=re.compile("DeclRefExpr")
regx_CXXBindTemporaryExpr=re.compile("CXXBindTemporaryExpr")
regx_CXXConstructExpr=re.compile("CXXConstructExpr")
regx_CXXMethodDecl=re.compile("CXXMethodDecl +<line")
regx_CXXMethodDecl1=re.compile("CXXMethodDecl")
regx_TypedefDecl=re.compile(".*TypedefDecl ([\s\S]*?)\n(?=Dumping)")
regx_instantiation=re.compile(".*CompoundStmt (\w+) <line.*>\n([\s\S]*?)\n(?=(.*)CompoundStmt)")

# f_ast=re.sub(regx_TypedefDecl,"",f_ast.read())
# regx=re.compile("ImplicitCastExpr" or "CXXMemberCallExpr" or "CXXThisExpr" or "DeclRefExpr" or "CXXBindTemporaryExpr")
regx_line=re.compile("<line:\d+:\d+, col:\d+>")
regx_IntegerLiteral=re.compile("IntegerLiteral")
regx_h2d=re.compile("\d{4,10}")
regx_FieldDecl=re.compile("FieldDecl")
regx_ParmVarDecl=re.compile("ParmVarDecl")
regx_CXXCtorInitializer=re.compile("CXXCtorInitializer")
regx_referenced=re.compile("referenced")

regx_more=re.compile("<.*'>'")
regx_more1=re.compile("<.*'>='")
# pos=""
# neg=""
# regx_pos=re.compile("(.*\.pos([\s\S\n]*?)\->(\w+))")
# regx_neg=re.compile("(.*\.neg([\s\S\n]*?)\->(\w+))")
# pos=pos+regx_pos.search(txt).group(3)+""
# neg=neg+regx_neg.search(txt).group(3)+""
# print(pos)
# print(neg)

regx_NullStmt=re.compile("NullStmt")
regx_pos_MemberExpr=re.compile("MemberExpr.*\.pos")
regx_neg_MemberExpr=re.compile("MemberExpr.*\.neg")
regx_MemberExpr=re.compile("MemberExpr.*lvalue ->(\w+)")

always_part=0
p=0
n=0
pos=""
neg=""
always_sensi=""
txt1=str(regx_TypedefDecl.search(txt).group(1))
print(txt1)
for line in txt1.split("\n"):
    if regx_NullStmt.search(line):
        if len(pos)+len(neg)>0:
            # print(pos,neg)
            pos = pos[:-1]
            neg = neg[:-1]
            always_sensi=always_sensi+"sensitive: "+str(pos)+";"+str(neg)+"\n"

            pos=""
            neg=""
        # if always_part==1:
        #
        always_part=1
    elif regx_pos_MemberExpr.search(line):
        p=1
    elif regx_neg_MemberExpr.search(line):
        n=1
    elif regx_MemberExpr.search(line):
        regx_MemberExpr_obj=regx_MemberExpr.search(line)
        if always_part==1 and p==1:
            pos=pos+str(regx_MemberExpr_obj.group(1))+","
            p=0
        elif always_part==1 and n==1:
            neg=neg+str(regx_MemberExpr_obj.group(1))+","
            n=0
# print(pos,neg)
pos=pos[:-1]
neg=neg[:-1]
always_sensi=always_sensi+"sensitive: "+str(pos)+";"+str(neg)+"\n"
print(always_sensi)
new_ast_code.write(always_sensi)







##实例化部分
if regx_instantiation.search(txt,1):
    regx_instantiation_obj=regx_instantiation.search(txt)
    if regx_instantiation_obj.group(0).count("CompoundStmt")>1 :  ##排除不是实例化的情况
        txt = re.sub(regx_TypedefDecl, "", txt)
    else:
        txt=re.sub(regx_TypedefDecl,regx_instantiation_obj.group(0),txt)
else:
    txt=re.sub(regx_TypedefDecl,"",txt)
# txt=re.sub(regx_TypedefDecl,"",txt)



for line in txt.split("\n"):
    # line=re.sub("\\d{1,2}(;\\d{1,2})?", "",line)
    # print(line,"..")

    line=re.sub("0x\w+","",line)
    line=re.sub("referenced","",line)


    if  regx_CXXMemberCallExpr.search(line) or regx_CXXThisExpr.search(line) or\
            regx_DeclRefExpr.search(line) or regx_CXXBindTemporaryExpr.search(line) or regx_CXXConstructExpr.search(line) or \
            regx_CXXCtorInitializer.search(line) or regx_CXXMethodDecl.search(line) :
        pass

    else:
        if regx_line.search(line) or regx_FieldDecl.search(line) or regx_ParmVarDecl.search(line) or regx_CXXMethodDecl1.search(line):
            if regx_CXXMethodDecl1.search(line):
                line = re.sub("parent.*used", "", line)
            elif regx_ParmVarDecl.search(line):
                line = re.sub("<.*used", "", line)
            pass
        else:
            ##此处过滤“<.*>”，对大于号进行保护，避免被滤除
            if regx_more.search(line) or regx_more1.search(line):
                line=line
            else:
                line=re.sub("<.*>","",line)
        if regx_IntegerLiteral.search(line):
            if regx_h2d.search(line):
                number = int(regx_h2d.search(line).group())
                line=re.sub(regx_h2d,"%s"%hex(number),line)
        else:pass
        new_ast_code.write(line+"\n")


# new_ast_code.write("pos:"+pos)

# new_ast_code.write("neg:"+neg)
