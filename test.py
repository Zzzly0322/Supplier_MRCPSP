
# coding=gbk

import numpy as np
import matplotlib.pylab as plt
from pylab import * #图像中的title,xlabel,ylabel均使用中文
x=["J14","J16","18","J20","J30"]


# y3=[49,44,32,28,17,12,15,5,80,80,80]

ruba00=[8.42,18.78,25.48,31.09,35.84]
ruba01=[21.93,36.91,42.74,37.23,47.75]
ruba02=[44.93,47.99,48.82,56.88,57.30]

cost00=[0.87,5.34,6.47,10.20,7.96]
cost01=[11.02,13.52,13.12,14.11,18.04]
cost02=[17.16,18.33,20.58,24.08,25.82]

ruba0=[ruba00,ruba01,ruba02]
cost0=[cost00,cost01,cost02]
y1=ruba0
matplotlib.rcParams["font.family"]="Kaiti"
matplotlib.rcParams["font.size"]=20



# ax1 = plt.subplot() # 使用subplots()创建窗口
# ax1.bar(x, y1[2],color= 'green',alpha=0.4,width=0.5,label="max")
# ax1.bar(x, y1[1], color='red',alpha=0.4,width=0.5,label="avg")
# ax1.bar(x, y1[0], color='blue',alpha=0.4,width=0.5,label="min")

plt.show()

#创建一个figure画图对象

# plt.show()