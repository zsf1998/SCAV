#### Clang-check的安装和使用

一、clang安装

1、在linux中直接使用apt查找可安装clang版本

```
sudo apt-cache search clang
```

2、输入上一条命令后，就查找出所有与clang相关的软件工具，根据自己的虚拟机找到相同版本的clang和clang-tools（我安装的是clang-12和clang-tools-12），然后进行安装

```
sudo apt-get install clang-12

sudo apt-get install clang-tools-12
```

3、安装clang和clang-tools后，clang-check就可以使用，利用--help查看clang-check的选项参数，根据需求选择需要的选项

```
clang-check-12 --help
```



二、clang-check使用

根据clang-check的选项参数选择，输入以下命令就可以解析出AST

```
clang-check-12 -ast-dump --color=0 -ast-dump-filter=halfadder /home/jy/systemcfile/halfadder.cpp -- -I/home/jy/systemc-2.3.3/include |sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g" |sed -r "s:\x1B\[0-9;]*[mk]::g" |sed "s,\x1B\[[0-9;]*[a-zA-Z],,g" > /home/jy/ASTfile/halfadder.txt
```

命令说明：

```
-ast-dump                              //生成AST
-ast-dump-filter=halfadder             //对生成的AST进行限制，限制条件是只输出与halfadder相关内容
```

```
/home/jy/systemcfile/halfadder.cpp     //输入文件路径
-I/home/jy/systemc-2.3.3/include       //systemc路径
```

下面的命令是删除转义字符、颜色字符等特殊字符，使用clang-check解析出的AST出含有大量的转义字符、颜色字符等特殊字符，重定向输出无法正常使用，因此需要对其中的转义字符、颜色字符等特殊字符进行删除（以下三种删除规则可以根据需要选择）

```
|sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g" 
|sed -r "s:\x1B\[0-9;]*[mk]::g" 
|sed "s,\x1B\[[0-9;]*[a-zA-Z],,g"
```

```
> /home/jy/ASTfile/halfadder.txt     //输出重定向
```

