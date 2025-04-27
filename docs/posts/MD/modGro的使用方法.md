---
categories:
    - Computational Chemistry
date: 2025-04-26
tags:
    - Computational Chemistry
    - Molecular Dynamics Simulation
comments: true
---

# modGro的使用方法

本篇文章主要用于说明modGro的使用方法。

<!-- more -->

### modGro的简要介绍

modGro是专门用于处理GROMACS生成的`gro`文件的工具。modGro可在其[主页](https://github.com/luck19990920/Scripts/tree/master/modGro){:target="_blank"}上进行下载。下载得到的文件夹中，`modGro`是在Linux系统中的可执行文件，`modGro.exe`为在Windows系统中的可执行文件。modGro支持修改gro文件中特定的残基名和原子名、删除特定的残基、复制特定的残基、对残基进行位置变换和合并多个gro文件等操作。以下通过一些例子来说明modGro的使用方法。文中涉及到的文件可在[此处](./files.zip)下载。

### 例子1：修改特定的残基名与原子名
`solv.gro`为一个含有528个水分子的gro文件。打开modGro后，依次键入如下的内容(`//`后的是注释)可以将1,2,9-30号残基的名字改为`MOL`。
```
solv.gro                 // 载入solv.gro
3                        // 修改残基名或原子名
1                        // 修改残基名
1,2,9-30                 // 需要修改的残基序号为1,2,9-30(残基序号从1开始)
MOL                      // 修改的残基名为MOL
4                        // 输出gro文件
fix-1.gro                // 输出到fix-1.gro
q                        // 退出程序
```
此时，序号为1,2,9-30的残基的残基名已经由`SOL`被修改为`MOL`。修改后的结构被保存到`fix-1.gro`文件中。

还是对于`solv.gro`文件，打开modGro后，依次键入如下的内容(`//`后的是注释)可以将1,10,18-20号残基中的第一个原子的原子名修改为`HA`。
```
solv.gro                 // 载入solv.gro
3                        // 修改残基名或原子名
2                        // 修改原子名
2                        // 根据残基序号进行修改
1,10,18-20               // 需要修改的残基序号为1,10,18-20(残基序号从1开始)
1                        // 修改残基中的第一个原子的原子名
HA                       // 修改成的原子名为HA
0                        // 返回主菜单
4                        // 输出gro文件
fix-2.gro                // 输出到fix-2.gro
q                        // 退出程序
```
此时，序号为1,10,18-20的残基中的第一个原子的原子名已经由`OW`被修改为`HA`。修改后的结构被保存到`fix-2.gro`文件中。
### 例子2：将单层COF结构拓展成多层COF结构
`COF.gro`为某一COF材料的gro文件(如下图所示)。我们的目标是采用modGro将该单层COF结构拓展成5层COF结构，并且层与层之间的间距为5埃。
<figure markdown="span">
  ![](COF-1.bmp){ width="600" }
</figure>
首先，双击点开`modGro.exe`，然后将`COF.gro`拖进窗口中并回车。窗口中将显示如下的gro文件信息。
```
Cell information
In Angstrom:
Cell vector 1,  X=  22.50600  Y=   0.00000  Z=   0.00000  Norm=  22.50600
Cell vector 2,  X=   0.00000  Y=  38.98150  Z=   0.00000  Norm=  38.98150
Cell vector 3,  X=   0.00000  Y=   0.00000  Z=  10.00000  Norm=  10.00000
Cell angles:
  Alpha=  90.00000  Beta=  90.00000  Gamma=  90.00000 degree
  Total atoms:    240
Total residue:    1
```
上述的文件信息表明：该gro文件中的盒子是正交的，并且盒子的三边长分别为22.50600埃、38.98150埃和10.00000埃。盒子三边的三个夹角都为90度。该gro文件中的原子总数为240，有1个残基。
!!! note "小贴士"

    在Windows下，也可以不双击点开`modGro.exe`，而用鼠标左键将`COF.gro`放置到`modGro.exe`上面后放开鼠标左键。这样可以直接使`modGro.exe`载入`COF.gro`文件进行分析。在Linux下，可直接在命令行中输入`modGro test.gro`回车即可将`test.gro`载入`modGro`中。

随后，根据屏幕上所示，键入功能前面的数字而实施特定的功能。
```
'q': Exit program gracefully                   'r': Load a new file

        ******************** Main function menu ********************

1 Show residue information
2 Geometry operation on the present system
3 Modify the residue or atom names
4 Output current structure to .gro file
```
在这里，键入`2`后，以下的内容将出现在窗口中。
```
0 Return
1 Translate selected residues according to a translation vector
2 Rotate selected residues around an axis
3 Clone residues
4 Remove residues
5 Set cell information
6 Merge multiple .gro file
7 Check residues coordinate information
```
若键入

* `0`：回到上一级
* `1`：对特定的残基进行平移
* `2`：对特定的残基进行旋转
* `3`：复制特定的残基
* `4`：删除特定的残基
* `5`：修改盒子的信息
* `6`：合并多个gro文件
* `7`：查看相关的原子坐标

在这里，操作思路是先将单层的COF结构复制4次，然后依次对这些单层的COF结构进行平移。为实现将单层的COF结构复制4次，首先键入`3`。然后再键入`1`即可对单层的COF膜复制一次。此时，返回到主菜单，然后键入`1`，然后再键入`1`，可以发现窗口中残基的个数变为了2个，原子的个数由之前的240变为了480，如下所示。
```
    1MOL     O1    1   0.256   0.435   0.488
    1MOL     O2    2   1.382   2.384   0.488
    1MOL     C3    3   0.121   1.259   0.505
    1MOL     C4    4   1.246   3.208   0.505
    1MOL     O5    5   0.111   0.610   0.480
    1MOL     O6    6   1.236   2.559   0.480
    1MOL     C7    7   1.162   0.379   0.505
    1MOL     C8    8   0.252   1.216   0.505
    1MOL     C9    9   0.037   2.328   0.505
    1MOL    C10   10   1.378   3.165   0.505
    1MOL    C11   11   0.413   1.036   0.505
    1MOL    C12   12   1.539   2.985   0.505
    1MOL    C13   13   1.087   0.149   0.505
    1MOL    C14   14   1.692   0.843   0.505
    1MOL    O15   15   0.829   1.535   0.487
    1MOL    O16   16   1.955   3.484   0.487
    1MOL    C17   17   0.526   1.121   0.505
    ......
    2MOL   O225  465   0.836   2.380   0.577
    2MOL   C226  466   0.354   3.265   0.507
    2MOL   O227  467   1.368   0.564   0.505
    2MOL   O228  468   0.195   1.486   0.505
    2MOL   O229  469   0.242   2.513   0.505
    2MOL   O230  470   1.320   3.435   0.505
    2MOL   N231  471   1.069   0.284   0.505
    2MOL   N232  472   0.288   1.087   0.505
    2MOL   N233  473   2.194   2.233   0.505
    2MOL   N234  474   1.413   3.036   0.505
    2MOL   C235  475   1.249   0.609   0.505
    2MOL   C236  476   0.097   1.405   0.505
    2MOL   C237  477   0.123   2.558   0.505
    2MOL   C238  478   1.222   3.354   0.505
    2MOL   C239  479   1.134   0.515   0.505
    2MOL   C240  480   0.009   2.464   0.505
```
按照上面的方法，再对1号残基复制3次即可得到5层COF结构。随后，对2号残基沿着z方向平移5埃，对3号残基沿着z方向平移10埃，对4号残基沿着z方向平移15埃，对5号残基沿着z方向平移20埃，并对盒子z方向上的尺寸进行适当的增加。执行该操作可键入如下的内容(`//`后的是注释)：
```
// 回到主菜单
2                    // 对体系进行结构变换
1                    // 对特定的残基进行平移操作
2                    // 对2号残基进行平移
0,0,5                // 平移的矢量为0,0,5(单位为埃)
1                    // 对特定的残基进行平移操作
3                    // 对3号残基进行平移
0,0,10               // 平移的矢量为0,0,10(单位为埃)
1                    // 对特定的残基进行平移操作
4                    // 对4号残基进行平移
0,0,15               // 平移的矢量为0,0,15(单位为埃)
1                    // 对特定的残基进行平移操作
5                    // 对5号残基进行平移
0,0,20               // 平移的矢量为0,0,20(单位为埃)
5                    // 修改盒子尺寸
22.50600,0,0         // 第一个轴对应的矢量为22.50600,0,0(单位为埃)
0,38.98150,0         // 第二个轴对应的矢量为0,38.98150,0(单位为埃)
0,0,30               // 第三个轴对应的矢量为0,0,30(单位为埃)
0                    // 返回主菜单
4                    // 输出gro文件
[回车]               // 输出到modGro.exe所在目录
q                    // 退出程序
```
此时，在`modGro.exe`所在目录下会生成`fix.gro`，该文件就是最终得到的gro文件。将该gro文件利用VMD可视化，如下图所示。此时COF结构已经由最初的1层拓展至5层，并且层与层之间的间隔为5埃。
<figure markdown="span">
  ![](COF-2.bmp){ width="500" }
</figure>

### 例子3：对多个gro文件进行合并
本例子将在例子2的基础上沿着z轴在COF结构的左侧添加水溶液。`solv.gro`为一个三边尺寸分别为22.50600，38.98150和20(单位为埃)的水盒子。首先，将`solv.gro`利用modGro把其z方向的盒子尺寸由20埃变为50埃(因为上述得到的`fix.gro`的z方向上的盒子尺寸为30埃)。执行该操作可键入如下的内容(`//`后的是注释)：
```
solv.gro                  // 载入solv.gro文件
2                         // 对体系进行结构变换
5                         // 修改盒子尺寸
22.50600,0,0              // 第一个轴对应的矢量为22.50600,0,0(单位为埃)
0,38.98150,0              // 第二个轴对应的矢量为0,38.98150,0(单位为埃)
0,0,50                    // 第三个轴对应的矢量为0,0,50(单位为埃)
0                         // 返回主菜单
4                         // 输出gro文件
extend_solv.gro           // 输出到extend_solv.gro文件中
q                         // 退出程序
```
将`extend_solv.gro`可视化如下所示。
<figure markdown="span">
  ![](COF-3.bmp){ width="500" }
</figure>
随后，修改`fix.gro`的盒子信息，使其与上述的`extend_solv.gro`中的盒子信息保持一致，并且将COF结构整体沿着z方向平移20埃。执行该操作可键入如下的内容(`//`后的是注释)：
```
fix.gro                    // 载入fix.gro文件
2                          // 对体系进行结构变换
5                          // 修改盒子尺寸
22.50600,0,0               // 第一个轴对应的矢量为22.50600,0,0(单位为埃)
0,38.98150,0               // 第二个轴对应的矢量为0,38.98150,0(单位为埃)
0,0,50                     // 第三个轴对应的矢量为0,0,50(单位为埃)
1                          // 对残基进行平移
[回车]                     // 对所有的残基进行平移
0,0,20                     // 平移的矢量为0,0,20(单位为埃)
0                          // 返回主菜单
4                          // 输出gro文件
extend_fix.gro             // 输出到extend_fix.gro文件中
q                          // 退出程序
```
将`extend_fix.gro`可视化如下所示。
<figure markdown="span">
  ![](COF-4.bmp){ width="500" }
</figure>
!!! info "注意"

    若采用modGro合并盒子尺寸不同的多个gro文件并且不在modGro中修改盒子的尺寸，最终得到的盒子尺寸为载入的第一个gro文件中的盒子尺寸。

最后，将`extend_solv.gro`与`extend_fix.gro`使用`modGro`进行合并。执行该操作可键入如下的内容(`//`后的是注释)：
```
extend_solv.gro              // 载入extend_solv.gro文件
2                            // 对体系进行结构变换
6                            // 合并gro文件
extend_fix.gro               // 需要将extend_fix.gro进行合并
0                            // 返回主菜单
4                            // 输出gro文件
merge.gro                    // 输出到merge.gro文件中
q                            // 退出程序
```
将`merge.gro`可视化如下所示。
<figure markdown="span">
  ![](COF-5.bmp){ width="500" }
</figure>

### 附：对于modGro内部实现的一些说明

modGro的实现过程中采用了面向对象编程(OOP)的方法。在这之中，存在三个类，并且这三个类是层层继承的关系。`reside`类中使用到了`def_vector`类的相关性质，而`GRO`类中使用到了`reside`类的相关性质，如下图所示。
<figure markdown="span">
  ![](class.png){ width="500" }
</figure>
这三个类的作用如下：

* `def_vector`：三维矢量的类。矢量的平移、旋转以及矢量之间的夹角在此类中进行实现。
* `reside`：单个残基的类。`gro`文件中的每一个残基都为该类的一个实例。该类中有三个属性，分别为`resname`(该残基的残基名)、`atom_name_reside`(残基中的原子名数组)与`coordinate_reside`(残基中的原子坐标数组)。在这之中，`coordinate_reside`中的每一个元素都为`def_vector`实例。
* `GRO`：gro文件的类。该类主要用于将gro文件中的盒子信息、残基序号、残基名、原子名和原子坐标等信息组织起来。

`GRO`类中保存`gro`文件中的信息采用了关联数组(即字典)。键为残基的序号，而值为残基的信息。如下图所示。
<figure markdown="span">
  ![](class-1.png){ width="500" }
</figure>


