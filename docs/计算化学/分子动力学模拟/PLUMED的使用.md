---
comments: true
---

`PLUMED`是用于分子动力学模拟增强采样与自由能计算的程序。该程序的官网为<a href="https://www.plumed.org/" target="_blank">https://www.plumed.org/</a>。在其的官网上有丰富的<a href="https://plumed-school.github.io/browse.html" target="_blank">案例</a>可以学习。对于分子动力学模拟而言，计算自由能的一般思路是根据分子动力学模拟获得的轨迹建立统计直方图并估算概率的方法来计算分子不同状态间的自由能差。例如，在温度为$T$下，体系有两种状态A与B。根据分子动力学模拟获得的轨迹可以计算体系处于状态A与B的概率分别为$p_{A}$与$p_{B}$，那么体系从A转化到B的自由能变化$\Delta$$G_{A \rightarrow B}$为：
$$
    \Delta G_{A \rightarrow B} = G_{B} - G_{A} = - k_{B} T \ln \frac{p_{B}}{p_{A}}
$$
上式中$k_{B}$为玻尔兹曼常数。对于上式而言，若A转换到B的能垒很大时，则在可接受的模拟时间尺度内，在轨迹中观察到大量的从A到B的转化是相当困难的。这将会导致无法准确统计$p_{A}$与$p_{B}$，从而影响计算的准确性。

!!! note "注意"
    目前，超算上有两个版本的`PLUMED`供大家使用。一个版本是<strong>打了`PLUMED`补丁的`GROMACS`</strong>，另一个是<strong>单独的`PLUMED`</strong>。对于打了`PLUMED`补丁的`GROMACS`，该版本的`PLUMED`主要用来进行实施模拟过程中的增强采样操作，而对于单独的`PLUMED`，该版本主要用来实施`GROMACS`已经模拟完成获得轨迹后的轨迹分析操作。

### 打了`PLUMED`补丁的`GROMACS`的使用方法
打了`PLUMED`补丁的`GROMACS`主要用来在`GROMACS`模拟的过程中调用`PLUMED`而计算自由能。若需要调用`PLUMED`，需要给`PLUMED`传入一个输入文件(下列叙述中`PLUMED`的输入文件名默认为`plumed.dat`)。`plumed.dat`中确定了需要`PLUMED`完成的计算任务，相关字段可参见<a href="../../file/plumed-manual.pdf" target="_blank">`PLUMED`手册</a>。由于`PLUMED`中进行增强采样的算法有很多，因此这里不展开进行叙述。下面举一个关于打了`PLUMED`补丁的`GROMACS`的使用方法的例子。

* 背景介绍
  
  利用亚纳米孔道进行离子分离是目前的一个研究热点。由于亚纳米孔道的尺寸很小，因此离子并不容易进入孔道中。这导致大部分离子都处于亚纳米孔道外侧，而亚纳米孔道中离子出现的概率较少。而为了研究离子在孔道中的相关性质，我们就必须使用增强采样技术将离子推进孔道中，以此来提高采样的准确性和充分性。

* 实施细节
  
  下图是不采用和采用增强采样获得的离子在不同区域出现的频率。
  <div style='text-align:center'><img src='../../img/plumed_2.png' alt='此图无法显示' /></div>
  <div style='text-align:center'>离子在不同区域出现的频率</div>
  上述结果说明，当采用增强采样后，离子在孔道内外出现的频率无明显的差别。上述结果是在`PLUMED`中进行SMD(Steered MD)获得的。完成该任务的`plumed.dat`文件示例内容如下：
  ``` title="plumed.dat文件示例"
  # 选出index.ndx文件中MOL组中的所有原子，需要注意的是该路径下一定要存在index.ndx文件，否则会报错
  channel: GROUP NDX_FILE=index.ndx NDX_GROUP=MOL
  # 获得channel这个整体的质心
  c1: CENTER ATOMS=channel
  # 获得1号原子与channel这个整体的质心之间的距离，不使用周期性边界条件
  d: DISTANCE ATOMS=c1,1 NOPBC COMPONENTS
  # 设定SMD的相关设置
  restraint: ...
        MOVINGRESTRAINT
        # 需要施加偏置势的量为距离在z方向上的分量
        ARG=d.z
        # 第0步时，距离在z方向上的分量的理想值为1 nm，施加的偏置势为0 kJ/mol/nm^2
        AT0=1    STEP0=0      KAPPA0=0
        # 第5000步时，距离在z方向上的分量的理想值为1 nm，施加的偏置势为1000 kJ/mol/nm^2
        # 在0步至5000步中，偏置势线性增加
        AT1=1    STEP1=5000   KAPPA1=1000
        # 在第10000步，距离在z方向上的分量的理想值为-1 nm，施加的偏置势为1000 kJ/mol/nm^2
        AT2=-1   STEP2=10000  KAPPA2=1000
  ...
  # 输出相关物理量至COLVAR文件中，每10000步输出一次
  PRINT STRIDE=10000 ARG=* FILE=COLVAR
  ```
  按照常规的做法在虚拟机中获得`GROMACS`的tpr文件后，可在超算中利用`Gmx_Plu.sh`命令调用打了`PLUMED`补丁的`GROMACS`。<br/>
  `Gmx_Plu.sh`命令的使用方法如下：<br/>
  `Gmx_Plu.sh [name of .tpr file] [name of PLUMED input file]`<br/>
  例如：`Gmx_Plu.sh test.tpr plumed.dat`

!!! info inline end "温馨提示"

    若不需要在模拟过程中调用`PLUMED`，请使用`SubGmx.sh`命令提交计算任务，不要使用`Gmx_Plu.sh`命令提交计算任务，否则运算的性能会受到损失。

### 单独的`PLUMED`的使用方法

`PLUMED`单独使用一般用于`GROMACS`模拟完成得到轨迹后，对轨迹的分析。下面是一个简单的例子。

* 背景介绍
  
  为探究某种化学物种在孔道中的分布，探究其在不同时间下距离孔道中轴线之间的距离是非常有必要的。该例子就是来计算这个量的。

* 实施细节
  
  `plumed.dat`文件示例内容如下：
  ``` title="plumed.dat文件示例"
  # 从index.ndx中读取这种化学物种
  ion: GROUP NDX_FILE=index.ndx NDX_GROUP=ion
  # 从index.ndx中读取孔道原子
  MOL: GROUP NDX_FILE=index.ndx NDX_GROUP=MOL
  # 获得孔道的质心
  c1: CENTER ATOMS=MOL 
  # 求这种化学物种与孔道质心之间的平均距离(只保留XY方向上的分量，舍弃Z方向上的分量)
  d1: XYDISTANCES GROUPA=ion GROUPB=c1 MEAN
  # 输出计算结果
  PRINT ARG=d1.mean STRIDE=1000 FILE=COLVAR
  ```
  随后，在含有要分析的`GROMACS`的xtc文件所在的目录执行`SubPlu.sh`命令即可单独使用`Plumed`。<br/>
  `SubPlu.sh`命令的使用方法如下：<br/>
  `SubPlu.sh [name of .xtc file] [name of PLUMED input file]`<br/>
  例如：`SubPlu.sh test.xtc plumed.dat`

!!! note "注意"
    `SubPlu.sh`命令执行`PLUMED`时并未调用`GPU`，因此可能会有一些慢。只要输出的文件中一直有数据在更新就没问题。出现以下类似的内容说明`PLUMED`计算完成。
    ```
    PLUMED: 1 Prepare dependencies                        500001     0.137395     0.000000     0.000000     0.000185
    PLUMED: 2 Sharing data                                   501     0.006504     0.000013     0.000006     0.000182
    PLUMED: 3 Waiting for data                               501     0.001033     0.000002     0.000000     0.000008
    PLUMED: 4 Calculating (forward loop)                     501     0.062603     0.000125     0.000091     0.000405
    PLUMED: 5 Applying (backward loop)                       501     0.009490     0.000019     0.000016     0.000029
    PLUMED: 6 Update 
    ```

### 参考材料

[1] <a href='https://www.plumed.org/doc-v2.8/user-doc/html/belfast-5.html' target='_blank'>Belfast tutorial: Out of equilibrium dynamics</a><br/>
[2] <a href='../../file/plumed-manual.pdf' target='_blank'>PLUMED手册</a>