read -p "input y/n:  " a
echo "a=${a}"

case $a in
	[yY])
	echo "yes"
	;;
	
	[nN])
	echo "no"
	exit 1
	;;
	*)
	exit 1
	;;
esac


#if $a in "y";then
#	echo "generate tb"
#else 
#	exit 1
#fi
