---
comments: true
---

最开始，我们是通过运行`main.py`文件来运行该程序的。因此，我们首先从`main.py`文件来理解代码的编写思想。

```python
from config import ShermoConfig
from easyShermo import run_all_shermo


def welcome():
    """
    主页面信息
    """
    hello = """
EasyShermo: A python script to automate the use of Shermo
Version 1.2.0  Release date: 2023-Jul-28
Developer: Kimariyb (kimariyb@163.com)
Address: XiaMen University, School of Electronic Science and Engineering
Official website: https://github.com/kimariyb/easy-shermo
    """
    # 输出主页面信息
    print(hello)
    # 在启动时就读取 settings.ini 并返回对象
    shermo_config = ShermoConfig()
    # 打印配置文件信息
    print(shermo_config)
    return shermo_config


def main():
    # 主页面
    shermo_config = welcome()
    # 运行主程序
    run_all_shermo(shermo_config)


if __name__ == '__main__':
    main()
```

在程序的开头，导入了一个类和一个函数，分别为`ShermoConfig`类与`run_all_shermo`函数。我们现在分别来细看这个类和这个函数的具体定义。首先是`ShermoConfig`类。

```python
class ShermoConfig:
    def __init__(self):
        pass

    def __str__(self):
        pass
```

#### `ShermoConfig`类

整个`ShermoConfig`类的定义中包括两大部分。第一部分为`__init__`方法，该方法的目的是初始化对象。当对象被创建后，这一部分的代码会自动执行。第二部分是`__str__`方法，该方法的目的是返回一个对象的具体描述。下面，我们首先来看`__init__`方法中的具体代码。

```python
        self.__settings_path = os.path.join(os.path.dirname(__file__), "settings.ini")
        # 创建 ini config 对象
        self.config = configparser.ConfigParser()
        # 设置注释前缀
        self.config.comment_prefixes = ';'
        # 读取 ini 文件的配置
        self.config.read(self.__settings_path)
        # 将配置返回成对象
        self.shermo_config = self.config['Shermo']
        # 获取配置项
        self.shermoPath = self.shermo_config.get('shermoPath')
        self.spFile = self.shermo_config.get('spFile')
        self.prtvib = self.config.get('Shermo', 'prtvib')
        self.T = self.config.get('Shermo', 'T')
        self.P = self.config.get('Shermo', 'P')
        self.sclZPE = self.config.get('Shermo', 'sclZPE')
        self.sclheat = self.config.get('Shermo', 'sclheat')
        self.sclS = self.config.get('Shermo', 'sclS')
        self.sclCV = self.config.get('Shermo', 'sclCV')
        self.ilowfreq = self.config.get('Shermo', 'ilowfreq')
        self.ravib = self.config.get('Shermo', 'ravib')
        self.imode = self.config.get('Shermo', 'imode')
        self.conc = self.config.get('Shermo', 'conc')
        self.outshm = self.config.get('Shermo', 'outshm')
        self.defmass = self.config.get('Shermo', 'defmass')
```

**第一行**是对私有属性`__settings_path`进行初始化。`__file__`为文件的路径。例如：

```python
In [1]: __file__
Out[1]: 'C:\\Users\\89732\\Desktop\\gro.py'
```

而`os.path.dirname(path)`的作用是去掉文件名，返回目录。综上，`os.path.dirname(__file__)`就是得到所处文件夹的绝对路径。`os.path.join(Path1, Path2)`用于文件路径的拼接。故第一行中属性`__settings_path`储存着`settings.ini`文件的绝对路径。

**第二行**是创建一个`config`对象。configparser是Python标准库中用来解析配置文件的模块。

**第三行**是设置配置文件中的注释前缀为`;`

**第四行**为读取配置文件。

**第五行**为将配置返回对象。

**其余的行**为获取配置文件中对应的值，并将该值赋予给`ShermoConfig`对应的属性。格式如下所示。

`self.[attribute]=self.config.get([section], [option])`

现在，让我们来看`__str__`方法中的具体代码。

```python
return f"The ShermoConfig is: shermoPath={self.shermoPath}, spFile={self.spFile}, prtvib={self.prtvib}, T={self.T}, " \
               f"P={self.P}, sclZPE={self.sclZPE}, sclheat={self.sclheat}, sclS={self.sclS}, sclCV={self.sclCV}, " \
               f"ilowfreq={self.ilowfreq}, ravib={self.ravib}, imode={self.imode}, conc={self.conc}, outshm={self.outshm}, " \
               f"defmass={self.defmass}"
```

该部分代码定义了对象的具体描述。

#### `run_all_shermo`函数

`run_all_shermo`函数在`easyShermo.py`中。故下面我们来解释`easyShermo.py`中的代码。其中，包括了4个类定义，2个函数定义。下面，我们首先对`ParserFactory`类进行说明。

```python
class ParserFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_parser(shermo_config: ShermoConfig):
        """
        工厂方法，创建一个 Parser 对象
        :param shermo_config: 配置文件对象
        :return:
        """
        if shermo_config.spFile == "1":
            return GaussianParser()
        elif shermo_config.spFile == "2":
            return OrcaParser()
        else:
            raise ValueError("Unknown sp file format")
```



代码中关于此类有一个方法。该方法为静态方法(对应方法定义上面一行的`@staticmethod`)。该方法中需要传入的变量为`shermo_config`，该变量是类`ShermoConfig`的一个对象。随后，代码根据配置文件中`spFile`的值生成不同的对象。若`spFile=1`，则对应的量化程序是Gaussian，此时生成一个关于Gaussian的对象`GaussianParser()`。而若`spFile`=2，则对应的量化程序是ORCA，此时生成一个关于ORCA的对象`OrcaParser()`。否则，抛出错误提示`ValueError`。

下面我们对`Parser`类进行说明。

```python
class Parser:
    def __init__(self):
        pass

    def find_energy(self, contents):
        """
        在文件内容中查找能量值
        """
        raise NotImplementedError

    def process_files(self, file_pattern):
        """
        处理匹配给定文件模式的所有文件，并返回单点能
        """
        raise NotImplementedError

    def get_sp(self):
        """
        得到单点能
        :return: 单点能
        """
        raise NotImplementedError
```

下面我们对`OrcaParser`类进行说明。

```python
class OrcaParser(Parser):
    def __init__(self):
        super().__init__()

    def find_energy(self, contents):
        """
        在文件内容中查找能量值
        """
        energy_regex = re.compile(r'FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)')
        energies = re.findall(energy_regex, contents)
        if energies:
            energy = str(energies[-1])
            return energy
        else:
            raise ValueError('No energy found')

    def process_files(self, file_pattern):
        """
        处理匹配给定文件模式的所有文件，并返回单点能
        """
        files = glob.glob(file_pattern)
        results = []

        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    contents = f.read()
                    energy = self.find_energy(contents)
                    results.append((os.path.basename(file), energy))
                    print(f'File: {file}, Energy: {energy}')
            except Exception as e:
                print(f'Error: Failed to read {file}: {e}')

        return results

    def get_sp(self):
        """
        获得 sp 目录下的所有 orca 文件的单点能
        :return: 所有文件的单点能量和文件名组成的列表
        """
        print()
        print('The single point energy: ')
        dir_path = os.path.join(os.getcwd(), 'sp')
        return self.process_files(os.path.join(dir_path, '*.out'))
```

我们可以发现`OrcaParser`类是`Parser`的子类。在对象初始化中，子类`OrcaParser`覆盖了父类`Parser`的`ini`，通过`super`又调用了父类的`ini`，确保子类和父类的`ini`都能正常运行。方法`find_energy`是为了获得能量值，在这之中利用了正则表达式。具体的含义如下所示。

```
\s:用于匹配单个空格符,包括Tab键和换行符
+:表示匹配前一个字符出现1次或多次
():代表一个组,findall会将不同组查到的元素按以元组形式返回
?:匹配前一个字符零次或一次
\d:与一个数字字符匹配,等价于[0-9]
\.:转义.
```

方法`process_files`处理匹配给定文件模式的所有文件，并返回单点能。`glob.glob(file_pattern)`函数匹配所有符合条件的文件，并将其以list的形式返回。`os.path.basename(path)`返回`path`最后的文件名。随后该文件名与对应的能量值打包成为一个元组被加入到`result`列表中。在`except`后加上了`as e`。`as e`作为可选参数，表示给异常类型起一个别名`e`，这样的好处是方便在`except`块中调用异常类型。方法`get_sp`是获得目录下所有ORCA文件的单点能。`os.getcwd()`是返回当前进程的工作目录。

`GaussianParser`类与`OrcaParser`类类似，这里不再展开解释。

#### 相关细节理解

①对于`__name__ == '__main__'`的理解

如果py文件作为模块被导入，那么`__name__`就是该py文件的文件名(也称模块名)；

如果py文件直接运行，那么`__name_-`默认等于字符串`'__main__'`。

②对于配置文件解析的configparser库

**生成配置文件**的代码如下

```python
import configparser                           #导入模块

config = configparser.ConfigParser()          #实例化一个对象

config["GROMACS"] = {                         
    'T': '300',
    'P': '1'    
}

config["ORCA"] = {
     'method': 'DFT',
     'functional': 'B3LYP',
     'basis_set': '6-311G'
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)
```

运行该代码后，得到的`config.ini`文件内容如下：

```
[GROMACS]
t = 300
p = 1

[ORCA]
method = DFT
functional = B3LYP
basis_set = 6-311G
```

**读取配置文件**的代码如下：

```python
import configparser

config = configparser.ConfigParser()                 #实例化一个对象

config.read('config.ini')                            #读取配置文件
sections = config.sections()                         #获取配置文件中所有的sections，以列表的形式返回
print(sections)

value = config.get('GROMACS', 't')                   #获取[GROMACS]下t字段对应的值
print(value)

item = config.items('ORCA')                          #获取[ORCA]下对应的键值对，返回形式[(keys, values)]
print(item)
```

运行该代码后，得到下列的结果。

```python
['GROMACS', 'ORCA']
300
[('method', 'DFT'), ('functional', 'B3LYP'), ('basis_set', '6-311G')]
```

**修改配置文件**的代码如下：

```python
import configparser

config = configparser.ConfigParser()                 #实例化一个对象

config.read('config.ini')
config.add_section('VASP')                           #增加VASP这个section

config.remove_section('GROMACS')                     #删除GROMACS这个section
config.remove_option('ORCA', 'method')               #删除ORCA这个section下的method字段

config.set('ORCA','functional','LDA')                #将ORCA这个section下的functional值设置为LDA
with open('config.ini', 'w') as configfile:
    config.write(configfile)
```

运行该代码后，得到的`config.ini`文件内容如下：

```
[ORCA]
functional = LDA
basis_set = 6-311G

[VASP]
```

③对于subprocess库的相关理解

subprocess库的作用是能够利用python程序去运行其他的程序或者命令。此外，subprocess库还能够重定向进程的输入与输出，这意味着我们能够控制什么数据被传入进程中和从进程中获取什么数据。

**Example 1:运行Shell命令**

`subprocess.run()`方法是一种简便运行子进程的方式，其将一直等待，直到子进程运行完成。其有以下的几个参数：

`args`：将要运行的命令和其的参数，以列表的形式传入。

`capture_output`：当设置为`True`时，将获取标准输出与标准错误。

`text`：当设置为`True`时，标准输出与标准错误将以字符串的形式输出，否则将以字节的形式输出。

`check`：布尔值。该值决定是否检查子进程的返回码(return code of the subprocess)。如果该值为`True`，如果返回码非零，将返回`CalledProcessError`错误。

`timeout`：秒数。在超时之前等待子进程完成的时间。

`shell`：布尔值。是否在shell中运行命令。这意味着命令是以字符串形式传递的，并且可以使用特定于shell的功能，如通配符扩展和变量替换。

`subprocess.run()`的结果是一个`CompletedProcess`对象。该结果有以下的属性。

`args`：运行的命令及其参数

`returncode`：子进程的返回码

`stdout`：标准输出

`stderr`：标准错误

```python
import subprocess

result = subprocess.run(["dir"], shell=True, capture_output=True, text=True)
print("args:")
print(result.args)
print("returncode:")
print(result.returncode)
print("stdout:")
print(result.stdout)
print("stderr:")
print(result.stderr)
```

输出如下：

```python
args:
['dir']
returncode:
0
stdout:
 驱动器 C 中的卷是 Windows-SSD
 ......
stderr:
    
```

**Example 2:运行python脚本**

创建一个名为test.py的python脚本，内容如下：

`print("Hello World")`

主程序的代码如下：

```python
import subprocess

result = subprocess.run(["python", "test.py"], shell=True, capture_output=True, text=True)
print("args:")
print(result.args)
print("returncode:")
print(result.returncode)
print("stdout:")
print(result.stdout)
print("stderr:")
print(result.stderr)
```

输出如下：

```python
args:
['python', 'test.py']
returncode:
0
stdout:
Hello World

stderr:
```

`subprocess.Popen()`是运行子进程的较低级别的接口，而`subprocess.run()`是`Popen`的较高级别的包装器，使用起来更方便。下面是`subprocess.Popen()`的一个例子。

```python
import subprocess

p = subprocess.Popen(["python", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

output, errors = p.communicate()

print(output)
```

输出结果如下：

```python
usage: python [option] ... [-c cmd | -m mod | file | -] [arg] ...
Options and arguments (and corresponding environment variables):
-b     : issue warnings about str(bytes_instance), str(bytearray_instance)
         and comparing bytes/bytearray with str. (-bb: issue errors)
-B     : don't write .pyc files on import; also PYTHONDONTWRITEBYTECODE=x
-c cmd : program passed in as string (terminates option list)
......
```

`Popen`类有一些方法能够用于对进程进行操作。例如`communicate()`、`poll()`、`wait()`、`terminate()`和`kill()`。使用`communicate()`能够分别将标准输出与标准错误存储至对应的变量。

------

参考材料

[1] <a href='https://zhuanlan.zhihu.com/p/90203080' target='_blank'>python `__name__=='__main__'`详细解释</a><br/>
[2] <a href='https://blog.csdn.net/happyjacob/article/details/109346625' target='_blank'>读写配置文件——configparser模块详解</a><br/>
[3] <a href='https://www.datacamp.com/tutorial/python-subprocess' target='_blank'>An Introduction to Python Subprocess: Basics and Examples