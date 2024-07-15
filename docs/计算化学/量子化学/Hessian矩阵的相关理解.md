---
comments: true
---

### 什么是Hessian矩阵

Hessian矩阵$H$是体系能量对原子坐标的二阶导数矩阵。对于含有$N$个原子的体系的Hessian矩阵，其是$3 N$维的。对于含有2个原子$A$和$B$的体系，其的Hessian矩阵如下所示。
$$H = 
\begin{bmatrix}
    \frac{\partial^2 E}{\partial x_A \partial x_B} & \frac{\partial^2 E}{\partial x_A \partial y_B} & \frac{\partial^2 E}{\partial x_A \partial z_B}\\\\
    \frac{\partial^2 E}{\partial y_A \partial x_B} & \frac{\partial^2 E}{\partial y_A \partial y_B} & \frac{\partial^2 E}{\partial y_A \partial z_B}\\\\
    \frac{\partial^2 E}{\partial z_A \partial x_B} & \frac{\partial^2 E}{\partial z_A \partial y_B} & \frac{\partial^2 E}{\partial z_A \partial z_B}\\\\
\end{bmatrix}
$$

### Gaussian中的Hessian矩阵

在Gaussian的fch文件中`Cartesian Force Constants`字段下即为Hessian矩阵。Hessian矩阵是对称矩阵，fch只记录了其三角部分。利用如下的Python代码能够读取这一部分。
``` py title="读取Hessian矩阵的三角部分" linenums="1" 
if line.startswith('Cartesian Force Constants'):
    num += 1
    ls = []
    while not lines[num].strip().split()[0].startswith('Dipole'):
        ls.extend(lines[num].strip().split())
        num += 1
    j = 0
    for m in range(3*natoms):
        for n in range(m+1):
            Hess[m, n] = float(ls[j])   # Hess为存储Hessian矩阵的数组
            j += 1
```
随后，可以使用如下的Python代码获得整个Hessian矩阵。
``` py title="获得整个Hessian矩阵" linenums="1"
Hess = Hess + Hess.T
for i in range(3*natoms):
    Hess[i, i] /= 2    # 对角元被算了2次
``` 
在此基础上，我们可以获得力常数矩阵$F$。力常数矩阵是把Hessian矩阵做质量权重的产物，如下式所示。下式中，$M$是质量矩阵，其也是$3 N$维的。其的1至3号对角元对应1号原子质量，4至6号对角元对应2号原子质量，7至9号对角元对应3号原子质量。
$$
F = M{^{-\frac{1}{2}}} H M{^{-\frac{1}{2}}} 
$$
$$
F_{i,j} = H_{i,j} / \sqrt{M_{i,i} M_{j,j}}
$$
采用以下的Python代码能够获得质量矩阵。
``` py title="构造质量矩阵" linenums="1"
massmat = np.zeros((3*natoms, 3*natoms))
for m in range(3*natoms):
    massmat[m, m] = atom_weight[m//3]
```
随后，我们可以按照上面的式子求得力常数矩阵$F$。
``` py title="计算求得力常数矩阵" linenums="1"
kmat = np.zeros((3*natoms, 3*natoms))
for i in range(3*natoms):
    for j in range(3*natoms):
        kmat[i, j] = Hess[i, j] / np.sqrt(massmat[i, i] * massmat[j, j])
```
将力常数矩阵$F$对角化后，可以得到$3 N$个<strong>本征值</strong>与$3 N$个<strong>本征矢</strong>。本征值为相应正则模式的力常数。由于直接基于Gaussian输出的Hessian矩阵得到的$\lambda$的单位是`Hartree/(Bohr^2 amu)`，因此在这里，需要将该值先转换为SI单位`J/(m^2 kg)`，然后通过以下的式子可以求得波数$k$。
$$
\nu_{i} = \frac{\sqrt{\lambda_{i}}}{2 \pi}
$$
$$
k = \frac{\nu_{i}}{c}
$$
$\lambda_{i}$有可能为负值。若$\lambda_{i}$为负值，则上式中采用其绝对值进行计算，并在最终计算得到的波数$k$前添加负号。
``` py title="获得波数" linenums="1"
eigenvals, eigenvects = np.linalg.eigh(kmat)

# 转换单位
amu2kg=1.66053878E-27
b2m=0.529177249E-10
au2J=4.35974434E-18
eigenvals = eigenvals * au2J / (b2m**2) / amu2kg

freq = np.zeros_like(eigenvals)
for i in range(len(eigenvals)):
    if eigenvals[i] > 0:
        freq[i] = np.sqrt(eigenvals[i]) / (2*np.pi)
    else:    # 对应为负号的情况
        freq[i] = -np.sqrt(-eigenvals[i]) / (2*np.pi)


wavenum = freq / 2.99792458E10
```

### ORCA中的Hessian矩阵
ORCA中的Hessian矩阵在hess文件中，下面是水分子在`B3LYP D3 def2-TZVP def2/J RIJCOSX`计算级别下计算得到的Hessian矩阵。
``` title="采用ORCA计算获得的水分子的Hessian矩阵"
 5.9567517884E-01  -7.7905601664E-02  -7.8412284217E-02  -8.3410358221E-02   1.1385908764E-01          1.1383542002E-01  -5.1226206512E-01  -3.5958323532E-02  -3.5428000001E-02
-7.7981786482E-02   2.5877636333E-01   2.5847445851E-01   7.1665830745E-02  -2.3668757846E-01         -2.3640435571E-01   6.3166934180E-03  -2.2091937751E-02  -2.2066155911E-02
-7.8488136634E-02   2.5847401511E-01   2.5845380488E-01   7.1680690283E-02  -2.3644496057E-01         -2.3643454464E-01   6.8081820768E-03  -2.2025113471E-02  -2.2022428532E-02
-8.3278602468E-02   7.1653703518E-02   7.1668811061E-02   9.9822995970E-02  -1.0675541456E-01          -1.0675437053E-01  -1.6544277567E-02   3.5103678794E-02   3.5087523568E-02
 1.1391193142E-01  -2.3667048881E-01  -2.3653277288E-01  -1.0675578428E-01   2.3792594227E-01          2.3778792808E-01  -7.1562093268E-03  -1.2584372174E-03  -1.2561139332E-03
 1.1388826756E-01  -2.3649175448E-01  -2.3641648061E-01  -1.0675473915E-01   2.3778792660E-01          2.3769677711E-01  -7.1335854329E-03  -1.2971298369E-03  -1.2832918101E-03
-5.1224960973E-01   6.3198683781E-03   6.8112698082E-03  -1.6544361377E-02  -7.1562500452E-03          -7.1336250662E-03   5.2879149150E-01   8.3929705827E-04   3.2530297013E-04
-3.5943704058E-02  -2.2104228093E-02  -2.2030380262E-02   3.5103700628E-02  -1.2584255588E-03          -1.2971493020E-03   8.3937351990E-04   2.3368625662E-02   2.3324372631E-02
-3.5413554597E-02  -2.2071391290E-02  -2.2035412540E-02   3.5087545730E-02  -1.2561334558E-03          -1.2832803355E-03   3.2537776998E-04   2.3324372621E-02   2.3324690254E-02
```
观察上述矩阵，我们发现其并不是对称矩阵。这是因为在构建交换相关项的静态二阶导数时仅包含了格点权重的一阶导数，导致了Hessian的对称性破缺。在这里，我们通过下面的方法进行数值处理。
``` py
hess = ( hess + hess.T ) / 2
```
其他处理方式和Gaussian中的Hessian矩阵处理方式一致。下面的Python代码展示了如何从ORCA计算得到的hess文件求得波数。
``` py title="通过ORCA的hess文件计算得到波数" linenums="1"
import numpy as np

file = input("Input path of a .hess file produced by ORCA\n")
with open(file, encoding="utf-8") as f:
    lines = f.readlines()
    for num, line in enumerate(lines):
        line = line.strip()
        if line == "$hessian":
            nhess = int(lines[num+1].strip()) # 获取Hessian矩阵的维数
            hess = np.zeros((nhess, nhess))  # 生成Hess矩阵模版
            for i in range(nhess):
                for j in range(nhess):
                    # 首先定位数据所在的行数
                    row_num = num + 2 + j // 5 *  (nhess + 1) + i + 1
                    # 再定位数据所在的列数
                    col_num = j % 5 + 1
                    # 提取数据
                    hess[i, j] = float(lines[row_num].strip().split()[col_num])
        
        if line == "$atoms":
            natoms = int(lines[num+1].strip())
            atom_m = np.zeros(natoms)
            for i in range(natoms):
                atom_m[i] = float(lines[num+2+i].strip().split()[1])
            break

# 对称Hessian矩阵后使用
hess = ( hess + hess.T ) / 2

# 构建质量矩阵
m_matix = np.zeros((nhess, nhess))
for i in range(nhess):
    m_matix[i, i] = atom_m[i//3]

# 获得力常数矩阵
kmat = np.zeros((nhess, nhess))
for i in range(nhess):
    for j in range(nhess):
        kmat[i, j] = hess[i, j] / np.sqrt(m_matix[i, i] * m_matix[j, j])

# 获得本征值与本征矢
eigenvals, eigenvects = np.linalg.eigh(kmat)

# 转换单位
amu2kg=1.66053878E-27
b2m=0.529177249E-10
au2J=4.35974434E-18
eigenvals = eigenvals * au2J / (b2m**2) / amu2kg

freq = np.zeros_like(eigenvals)
for i in range(len(eigenvals)):
    if eigenvals[i] > 0:
        freq[i] = np.sqrt(eigenvals[i]) / (2*np.pi)
    else:
        freq[i] = -np.sqrt(-eigenvals[i]) / (2*np.pi)

wavenum = freq / 2.99792458E10
print('Vibrational frequencies:')
for i in range(len(wavenum)):
    print(f'{i}: {wavenum[i]:>10.2f} cm**-1')
```
下面是通过上述程序计算得到的水分子的振动信息。
``` title="上述程序计算得到的水分子的振动信息"
Vibrational frequencies:
0:     -14.32 cm**-1
1:     -12.68 cm**-1
2:      -0.67 cm**-1
3:      19.86 cm**-1
4:      22.62 cm**-1
5:      32.73 cm**-1
6:    1616.41 cm**-1
7:    3781.10 cm**-1
8:    3885.68 cm**-1
```
``` title="ORCA的out文件中输出的水分子振动信息"
   0:         0.00 cm**-1
   1:         0.00 cm**-1
   2:         0.00 cm**-1
   3:         0.00 cm**-1
   4:         0.00 cm**-1
   5:         0.00 cm**-1
   6:      1616.39 cm**-1
   7:      3781.04 cm**-1
   8:      3885.61 cm**-1
```
对比两者的结果，我们可以发现上述程序计算得到的水分子的振动信息中含有6个较小的波数，这对应水分子的3个平动模式与3个转动模式，应该被无视掉。
### 参考材料
[1] <a href="http://sobereva.com/328" target="_blank">基于fch中的Hessian矩阵计算振动频率的简单程序Hess2freq</a>