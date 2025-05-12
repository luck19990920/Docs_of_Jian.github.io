---
categories:
    - Computational Chemistry
date: 2025-05-11
tags:
    - Computational Chemistry
    - Molecular Dynamics Simulation
    - Python
comments: true
slug: MDAnalysis_usage/
---

# MDAnalysis使用方法简介

本篇文章主要用于说明MDAnalysis的使用方法。

<!-- more -->

### MDAnalyis的安装

[MDAnalysis](https://www.mdanalysis.org/){:target="_blank"}是专门用于进行分子动力学模拟后处理的Python第三方库。若需使用该库，需要首先安装该库。该库能够在Linux、Windows以及macOS上使用。需要注意的是若在Windows上安装MDAnalysis时出现与Microsoft Visual C++ 14.0相关的报错，请先安装[Microsoft Visual Studio](https://visualstudio.microsoft.com/zh-hans/downloads/)后再安装MDAnalysis。下面演示在Windows下安装该库。

首先需安装Python。Python可在其[官网](https://www.python.org/)上下载得到。**安装Python的过程中请勾选Add python.exe to PATH，否则需手动将Python添加至环境变量。**手动将Python添加至环境变量的方法可参看[帖子](https://blog.csdn.net/Lyh1gguyg/article/details/146276117)。将Python添加至环境变量中的目的是使其在任意目录下都可启动。验证Python是否正确被添加至环境变量中的方法是在任意目录下打开cmd(按Win+R键，然后输入`cmd`)，然后输入`python`回车，若出现类似下面的内容则说明添加成功。
```
Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 19:29:22) [MSC v.1916 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
```
在Python已安装并且被添加至环境变量中的基础上，在cmd中键入`python -m pip install MDAnalysis`即可安装MDAnalysis库。Python中安装的第三方库可在cmd中键入`python -m pip list`查看。

### MDAnalyis的使用
简单来说，使用MDAnalysis分析每一帧数据的代码框架如下：
``` python linenums="1"
import MDAnalysis as mda
u = mda.Universe("test.gro","test.xtc") 
sel = u.select_atoms("resname NA")
for ts in u.trajectory:
    '''
    这里放置分析每一帧的代码
    '''
```
代码的第一行`import MDAnalysis as mda`是载入MDAnalysis库，并给其取一个别名`mda`(取啥名都行，只需要代码前后保持一致)。代码的第二行`u = mda.Universe("test.gro","test.xtc")`是调用该库中的Universe函数，并将该函数得到的结果返回给变量`u`。Universe函数是MDAnalysis中最重要的一个函数。该函数用于将相关的分子动力学模拟的文件载入MDAnalysis。传入Universe函数的参数众多，详情可看[Universe](https://docs.mdanalysis.org/2.9.0/documentation_pages/core/universe.html#MDAnalysis.core.universe.Universe)。由于一般情况下只需要修改该函数参数列表中的前2个参数，因此下面解释这两个参数。

* `topology`：该参数对应着分子动力学模拟结构文件的文件路径。这里传入的结构文件可以是gro文件或pdb等文件。
* `coordinates`：该参数对应着分子动力学模拟轨迹文件的文件路径。这里传入的参数可以是一个单帧的结构文件(例如gro文件)或多个单帧文件组合成的列表或多帧的轨迹文件(例如xtc文件或trr文件或xyz文件)。需要注意的是`topology`与`coordinates`传入的文件需匹配。
???+ 举例
    ```
    u = mda.Universe("test.gro","test.gro")                                  # 单帧轨迹分析
    u = mda.Universe("test.gro",["test1.gro", "test2.gro", "test3.gro"])     # 多个单帧轨迹分析
    u = mda.Universe("test.gro","test.xtc")                                  # 单个轨迹文件分析
    u = mda.Universe("test.gro",["test1.xtc", "test2.xtc", "test3.xtc"])     # 多个轨迹文件分析
    ```
代码的第三行用于选择出所需要研究的粒子。若没有这一行，则后续操作研究的是模拟盒子中的所有粒子。`u.select_atoms()`的括号中写入的是选择语句。选择语句的语法可参看[Atom selection language](https://userguide.mdanalysis.org/stable/selections.html)。这里选择出了所有残基名为NA的粒子。

`for ts in u.trajectory:`用于遍历每一帧。此外，还可以对`trajectory`使用Python中的切片操作。
???+ 举例
    * `for ts in u.trajectory[:10]:`：只分析前10帧
    * `for ts in u.trajectory[10:100]:`：只分析第10帧(包括)至100帧(不包括)(注：帧数从0开始计数)
    * `for ts in u.trajectory[::10]:`：每10帧分析一次

下面给出两个具体的例子说明MDAnalysis的用法。
#### 例子1：统计距离锂离子2埃至5埃的距离范围内水分子中O原子出现的平均个数
``` python title="版本1" linenums="1"
import MDAnalysis as mda
import numpy as np

u = mda.Universe("C:/Users/89732/Desktop/eq.gro","C:/Users/89732/Desktop/eq.xtc") 
OW = u.select_atoms("(name OW) and (around 5 (resname LI)) and not (around 2 (resname LI))", updating=True)
Li = u.select_atoms("resname LI")
result = []
for ts in u.trajectory:
    result.append(len(OW))

print(np.mean(np.array(result))/len(Li))
```
第1和2行用于导入MDAnalysis库与Numpy库。

第4行用于载入相关的分析文件。

第5行用于选择距离残基`LI`大于2埃但小于5埃的`OW`原子。值得注意的是，在这里使用了`updating=True`。这是开启了动态选区。若不开启动态选区，则遍历所有帧的过程中通过该选择语句得到的原子都恒定(很明显，在距离锂离子2埃至5埃的距离范围内OW原子在每帧中是变化的)。

第6行用于选择残基`LI`。

第7行的`result`为一个空列表，用于后续存放每一帧的数据。

第8和第9行用于遍历每一帧。其中`len(OW)`为该帧中使用选择语句得到`OW`中原子的个数。而`result.append(len(OW))`是将计算得到的`len(OW)`的值放入列表`result`最后。

第11行用于计算最终的结果并输出。`np.array(result)`是将列表`result`转化为`np.ndarray`类型，使其后续能够使用Numpy中的相关函数。`np.mean(x)`是求x这个`np.ndarray`类型的平均值。在这里`np.mean(np.array(result))`是平均每帧中符合要求的`OW`原子个数。将该值除以体系中总的残基`LI`的个数即得到平均每一个残基`LI`附近符合要求的`OW`原子个数。

上述的程序存在一个问题，即若体系很大，并且帧数很多，那么将不会立即得到最后的数据。为可视化MDAnalysis计算的进度，可添加一个进度条，实现的代码如下。
``` python title="版本2" linenums="1" hl_lines="3 9"
import MDAnalysis as mda
import numpy as np
from tqdm import tqdm

u = mda.Universe("C:/Users/89732/Desktop/eq.gro","C:/Users/89732/Desktop/eq.xtc") 
OW = u.select_atoms("(name OW) and (around 5 (resname LI)) and not (around 2 (resname LI))", updating=True)
Li = u.select_atoms("resname LI")
result = []
for ts in tqdm(u.trajectory):
    result.append(len(OW))

print(np.mean(np.array(result))/len(Li))
```
进一步，上述的程序还不够灵活。因为在程序中已经确定了需要统计的两个截断距离(即2埃和5埃)。为进一步提升代码的普适性，可做如下的调整。
```python title="版本3" linenums="1" hl_lines="4 6-12 14-17"
import MDAnalysis as mda
import numpy as np
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description="A Python script to calculate the average number of particles within a certain range from a certain ion")
parser.add_argument("-top", "--topology", type=str, help="topology file")
parser.add_argument("-tra", "--trajectory", type=str, help="trajectory file")
parser.add_argument("-i", "--ion", type=str, help="string of the selection of ions")
parser.add_argument("-a", "--atom", type=str, help="string of the selection of atoms")
parser.add_argument("-ra", "--ra", type=float, default=2.0, help="lower limit of statistical distance")
parser.add_argument("-rb", "--rb", type=float, default=5.0, help="upper limit of statistical distance")

args = parser.parse_args()
u = mda.Universe(args.topology, args.trajectory)
atoms = u.select_atoms(f"({args.atom}) and (around {args.rb} ({args.ion})) and not (around {args.ra} ({args.ion}))", updating=True)
ions = u.select_atoms(args.ion)

result = []
for ts in tqdm(u.trajectory):
    result.append(len(atoms))

print(np.mean(np.array(result))/len(ions))
```
上述代码中增加了对命令行参数解析的相关代码。完成命令行参数解析使用到了argparse库。该库的使用详见[argparse教程](https://docs.python.org/zh-cn/3/howto/argparse.html#)。

第4行用于导入argparse库。

第6行是使用argparse库的第一步，即创建一个`ArgumentParser`对象`parser`。后续argparse库的相关操作均围绕`parser`展开。

第7至12行用于添加参数。例如第7行添加了一个参数`-top`，并且该参数类型为`str`。该行的存在使得采用命令行运行该脚本时`-top`后的参数被赋值给`args.topology`。值得注意的是第11行和第12行的参数被设置了默认值。若命令行中不存在参数，则使用默认值，否则从命令行中获取。

第14行用于解析命令行参数。

第15至17行的代码用途与上一个版本中相关代码的用途一致。只是在该版本中，传入的参数并不是固定的，而是随着命令行参数的变化而变化。

若需运行该脚本，可在cmd中输入以下的命令回车即可。
``` python
python C:\Users\89732\Desktop\coor.py -top C:\Users\89732\Desktop\eq.gro -tra C:\Users\89732\Desktop\eq.xtc -i "resname LI" -a "name OW"
```

* `python`后紧跟着的是该Python脚本的文件路径
* `-top`后紧跟着的是分子动力学模拟结构文件的文件路径
* `-tra`后紧跟着的是分子动力学模拟轨迹文件的文件路径
* `-i`后紧跟的是离子对应的选择语句
* `-a`后紧跟的是所需统计粒子的选择语句

值得注意的是，上述命令中并未出现距离相关参数。这是因为在脚本中已设置了距离的默认值。若命令行中不传入`-ra`与`-rb`两个参数，则使用默认值。

!!! tip "注意"

    若需在命令行中查看Python脚本可以传入的参数，可以使用`-h`选项，即在命令行中输入`python C:\Users\89732\Desktop\coor.py -h`。下面是该选项对应的输出。
    ```
    usage: coor.py [-h] [-top TOPOLOGY] [-tra TRAJECTORY] [-i ION] [-a ATOM] [-ra RA] [-rb RB]

    A Python script to calculate the average number of particles within a certain range from a certain ion

    options:
    -h, --help                                show this help message and exit
    -top TOPOLOGY, --topology TOPOLOGY        topology file
    -tra TRAJECTORY, --trajectory TRAJECTORY  trajectory file
    -i ION, --ion ION                         string of the selection of ions
    -a ATOM, --atom ATOM                      string of the selection of atoms
    -ra RA, --ra RA                           lower limit of statistical distance
    -rb RB, --rb RB                           upper limit of statistical distance
    ```

#### 例子2：计算锂离子与水分子中O原子的径向分布函数

对于某些较为常用的统计项目，MDAnalysis已经设计了相关[模块](https://docs.mdanalysis.org/stable/py-modindex.html)来进行统计。这使得可以直接调用相关的MDAnalysis模块完成分析而无需自己写遍历每一帧的分析代码。

对于径向分布函数的计算可使用[`MDAnalysis.analysis.rdf`](https://docs.mdanalysis.org/stable/documentation_pages/analysis/rdf.html#module-MDAnalysis.analysis.rdf)这个模块来实现。
``` linenums="1" hl_lines="9-10"
import MDAnalysis as mda
from MDAnalysis.analysis import rdf
import matplotlib.pyplot as plt

u = mda.Universe("C:/Users/89732/Desktop/eq.gro","C:/Users/89732/Desktop/eq.xtc") 
OW = u.select_atoms("name OW")
Li = u.select_atoms("resname LI")

rdf_object = rdf.InterRDF(Li, OW, 200, (0,10))
rdf_object.run(verbose=True)

plt.plot(rdf_object.results.bins, rdf_object.results.rdf)
plt.xlabel(r"$r$($\AA$)")
plt.ylabel(r"RDF")
plt.xlim(0,10)
plt.show()
```
第9和10行是用于计算径向分布函数的关键代码。第9行使用`InterRDF`来计算径向分布函数。传入该函数的值有4个。前两个值为要统计径向分布函数的两个组。第三个值为计算径向分布函数的小区间的个数(默认值为75，在这里设置为200)，。第四个参数为径向分布函数横坐标的范围(单位为埃)。第10行使用`rdf_object.run(verbose=True)`开启计算。其中设置`verbose=True`是为了显示计算的进度。

计算完成后，`rdf_object.results.bins`中就为径向分布函数的横坐标的值，而`rdf_object.results.rdf`中就为径向分布函数的纵坐标的值。第12至16行是使用matplotlib直接作图。

#### 超算中MDAnalysis库的使用
超算中需进入本课题组的Python环境中才能够使用MDAnalysis库。本课题组在超算上的Python环境名为`hanbo`。目前该环境中已安装了Matplotlib、Numpy以及MDAnalysis等库。进入Python环境可在命令行中输入`anaconda`，若新出现的一行中以`(hanbo)`开头即进入了名为`hanbo`的Python环境。随后即可在此环境下运行Python代码(与在cmd中输入的命令一致)。若需退出该Python环境，可输入`exit_anaconda`。
