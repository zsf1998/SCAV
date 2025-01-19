python3 examples/example_parser.py test/$1.v > test/$1_ast.txt
if [ -s test/$1_ast.txt ]; then
	echo "Get ast successful!"
else
	echo "Ast empty!"
	exit 1
fi

python3 v2sc.py $1 > log/$1_log.txt
if [ -f "test/$1.cpp" -a -f "test/$1.hpp" ]; then
	echo "Successful tranalation!"
else
	echo "Translation failture!"
	exit 1
fi

read -p "If you need to generate the corresponding testbench, please enter(Y/N): " a

case $a in
	[yY])
	echo "yes"
	python3 tb_generate.py $1 > log/$1_tb_log.txt
	if [ -f "test/$1_driver.cpp" -a -f "test/$1_driver.hpp" -a -f "test/main.cpp" ]; then
		echo "Successfully generated tb!"
	else
		echo "Fail to generate tb!"
		exit 1
	fi
	;;
	
	[nN])
	echo "no"
	exit 1
	;;
	*)
	exit 1
	;;
esac

