##./SC2V.sh FILENAME MODULENAME
#set -e
#!/bin/bash
echo $1 $2;
if [ -n "$1" ]; then 
	echo "The FILENAME is current"	
else	
	echo "The FILENAME is error"	
	exit 1
fi

if [ -n "$2" ]; then 
	echo "The MODULENAME is current"	
else
	echo "The MODULENAME is error,please input modulename"	
	exit 1
fi	
	
		

clang-check-12  -ast-dump --color=0 -ast-dump-filter=$2 SystemCfile/$1.cpp -- -I/usr/local/systemc-2.3.3/include -ferror-limit=100 |sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g" |sed -r "s:\x1B\[[0-9;]*[mK]::g"  >ASTfile/$1.txt 
#echo $1 $2;

if [ -s ASTfile/$1.txt ]; then 
	echo "get AST successful"
else 
	echo "AST empty"
	exit 1	
fi	
	
	
python3 SC_ast_filter.py ASTfile/$1.txt >> log/log1.txt
python3 SystemC2Verilog2.py ASTfile/$1_new.txt >>log/log2.txt
mv -f ASTfile/$1_new.v Verilogfile
echo "$1.txt";
echo "$1_new.txt";
if [ -s Verilogfile/$1_new.v ]; then 
	echo "successful translation!"
else 
	echo "translation failure!"
	exit 1	
fi
