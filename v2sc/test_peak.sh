#for i in `seq 10`
#do
#     /usr/bin/time -f"peak memory is %Mkb" ./test_v2sc.sh SM3_controller
#done


/usr/bin/time -f"peak memory is %Mkb" python3 examples/example_parser.py test/$1.v > test/$1_ast.txt
if [ -s test/$1_ast.txt ]; then
	echo "Get ast successful!"
else
	echo "Ast empty!"
	exit 1
fi

/usr/bin/time -f"peak memory is %Mkb" python3 v2sc.py $1 > log/$1_log.txt
if [ -f "test/$1.cpp" -a -f "test/$1.hpp" ]; then
	echo "Successful tranalation!"
else
	echo "Translation failture!"
	exit 1
fi
