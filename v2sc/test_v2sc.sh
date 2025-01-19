for i in `seq 5`
do
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
done
