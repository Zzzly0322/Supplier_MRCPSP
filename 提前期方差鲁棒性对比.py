# coding=gbk
import matplotlib.pyplot as plt  # 导入绘图包
import matplotlib.pyplot as mp
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

ruba10=[15.44,19.74,25.04,25.47,33.94]
ruba11=[20.98,28.12,34.34,36.39,39.40]
ruba12=[34.83,43.24,43.28,46.82,49.61]

cost10=[1.88,6.47,5.94,9.83,10.81]
cost11=[11.06,11.43,13.25,14.00,15.51]
cost12=[16.95,19.33,18.55,20.41,26.42]

ruba1=[ruba10,ruba11,ruba12]
cost1=[cost10,cost11,cost12]

ruba20=[21.39,18.14,25.87,27.43,35.97]
ruba21=[26.42,27.81,31.99,36.06,45.20]
ruba22=[33.19,38.34,42.13,47.91,48.22]

cost20=[3.37,4.31,6.35,8.72,17.05]
cost21=[8.66,9.92,12.88,15.87,23.21]
cost22=[15.21,14.23,20.42,22.14,28.39]

ruba2=[ruba20,ruba21,ruba22]
cost2=[cost20,cost21,cost22]

def pyplot(y1,y2,i):
    matplotlib.rcParams["font.family"]="Kaiti"
    matplotlib.rcParams["font.size"]=20
    fig, ax1 = plt.subplots() # 使用subplots()创建窗口
    ax1.bar(x, y1[0], color='b',alpha=0.5,width=0.5, label="min")
    ax1.bar(x, [y1[1][j]-y1[0][j] for j in range(len(y1[0]))], color='r',alpha=0.5,width=0.5,label="avg",bottom=y1[0])
    ax1.bar(x, [y1[2][j]-y1[1][j] for j in range(len(y2[0]))], color='g', alpha=0.5,width=0.5, label="max", bottom= y1[1])

    # ax1.plot(x,y2[0],'*-.', c= 'b',label='项目成本节省度min', linewidth = 2) #绘制折线图像1,圆形点，标签，线宽
    # ax1.plot(x, y2[1], 'v:', c='b', label='项目成本节省度avg', linewidth=2)  # 绘制折线图像1,圆形点，标签，线宽
    # ax1.plot(x, y2[2], 'd--', c='b', label='项目成本节省度max', linewidth=2)  # 绘制折线图像1,圆形点，标签，线宽

    # ax1.plot(x, y3,'d--', c='firebrick',label='资源追加成本', linewidth = 2)



    mp.legend(loc=2,fontsize=16)

    # ax2 = ax1.twinx() # 创建第二个坐标轴
    # ax2.plot(x, y2, 'o-', c='blue',label='y2', linewidth = 1) #同上
    # mp.legend(loc=1)

    ax1.set_xlabel('项目规模大小-u∈[0，0.3]',size=20)
    ax1.set_ylabel('鲁棒性改善度（%）',size=20)
    # ax1.set_xticks()
    ax1.set_yticks([5,10,15,20,25,30,35,40,45,50,55,60])
    # # ax2.set_ylabel('y2', fontproperties=myfont,size=18)
    #自动适应刻度线密度，包括x轴，y轴

    plt.savefig("./out_file/"+str(i)+"鲁棒性 u=0.3.png", dpi=800, bbox_inches = 'tight')
    plt.show()


    fig2, ax2 = plt.subplots()
    ax2.bar(x, y2[0], color='#F9CDAD',width=0.5, label="min")
    ax2.bar(x, [y2[1][j]-y2[0][j] for j in range(len(y2[0]))], color='#83AF9B',width=0.5,label="avg",bottom=y2[0])
    ax2.bar(x, [y2[2][j]-y2[1][j] for j in range(len(y2[0]))], color='#FCB19A', width=0.5, label="max", bottom= y2[1])

    ax2.set_xlabel('项目规模大小-u∈[0，0.3]',size=20)
    ax2.set_ylabel('成本节省度（%）',size=20)
    # ax1.set_xticks()
    ax2.set_yticks([5,10,15,20,25,30])
    mp.legend(loc="best", fontsize=16)
    plt.savefig("./out_file/" + str(i) + "成本 u=0.3.png", dpi=800, bbox_inches='tight')
    plt.show()

pyplot(ruba0,cost0,1)


def pyplot2(y1,y2,i):
    matplotlib.rcParams["font.family"]="Kaiti"
    matplotlib.rcParams["font.size"]=20
    fig, ax1 = plt.subplots() # 使用subplots()创建窗口
    ax1.bar(x, y1[0], color='b',alpha=0.5,width=0.5, label="min")
    ax1.bar(x, [y1[1][j]-y1[0][j] for j in range(len(y1[0]))], color='r',alpha=0.5,width=0.5,label="avg",bottom=y1[0])
    ax1.bar(x, [y1[2][j]-y1[1][j] for j in range(len(y2[0]))], color='g', alpha=0.5,width=0.5, label="max", bottom= y1[1])

    mp.legend(loc="best",fontsize=16)

    # ax2 = ax1.twinx() # 创建第二个坐标轴
    # ax2.plot(x, y2, 'o-', c='blue',label='y2', linewidth = 1) #同上
    # mp.legend(loc=1)

    ax1.set_xlabel('项目规模大小-u∈[0.3，0.6]',size=20)
    ax1.set_ylabel('鲁棒性改善度（%）',size=20)
    # ax1.set_xticks()
    ax1.set_yticks([5,10,15,20,25,30,35,40,45,50,55,60])
    # # ax2.set_ylabel('y2', fontproperties=myfont,size=18)
    #自动适应刻度线密度，包括x轴，y轴

    plt.savefig("./out_file/"+str(i)+"鲁棒性 u=0.6.png", dpi=800, bbox_inches = 'tight')
    plt.show()


    fig2, ax2 = plt.subplots()
    ax2.bar(x, y2[0], color='#F9CDAD',width=0.5, label="min")
    ax2.bar(x, [y2[1][j]-y2[0][j] for j in range(len(y2[0]))], color='#83AF9B',width=0.5,label="avg",bottom=y2[0])
    ax2.bar(x, [y2[2][j]-y2[1][j] for j in range(len(y2[0]))], color='#FCB19A', width=0.5, label="max", bottom= y2[1])

    ax2.set_xlabel('项目规模大小-u∈[0.3，0.6]',size=20)
    ax2.set_ylabel('成本节省度（%）',size=20)
    # ax1.set_xticks()
    ax2.set_yticks([5,10,15,20,25,30])
    mp.legend(loc="best", fontsize=16)
    plt.savefig("./out_file/" + str(i) + "成本 u=0.6.png", dpi=800, bbox_inches='tight')
    plt.show()
pyplot2(ruba1, cost1, 2)



def pyplot3(y1,y2,i):
    matplotlib.rcParams["font.family"]="Kaiti"
    matplotlib.rcParams["font.size"]=20
    fig, ax1 = plt.subplots() # 使用subplots()创建窗口
    ax1.bar(x, y1[0], color='b',alpha=0.5,width=0.5, label="min")
    ax1.bar(x, [y1[1][j]-y1[0][j] for j in range(len(y1[0]))], color='r',alpha=0.5,width=0.5,label="avg",bottom=y1[0])
    ax1.bar(x, [y1[2][j]-y1[1][j] for j in range(len(y2[0]))], color='g', alpha=0.5,width=0.5, label="max", bottom= y1[1])

    mp.legend(loc="best",fontsize=16)

    # ax2 = ax1.twinx() # 创建第二个坐标轴
    # ax2.plot(x, y2, 'o-', c='blue',label='y2', linewidth = 1) #同上
    # mp.legend(loc=1)

    ax1.set_xlabel('项目规模大小-u∈[0.6，1.0]',size=20)
    ax1.set_ylabel('鲁棒性改善度（%）',size=20)
    # ax1.set_xticks()
    ax1.set_yticks([5,10,15,20,25,30,35,40,45,50,55,60])
    # # ax2.set_ylabel('y2', fontproperties=myfont,size=18)
    #自动适应刻度线密度，包括x轴，y轴

    plt.savefig("./out_file/"+str(i)+"鲁棒性 u=1.png", dpi=800, bbox_inches = 'tight')
    plt.show()


    fig2, ax2 = plt.subplots()
    ax2.bar(x, y2[0], color='#F9CDAD',width=0.5, label="min")
    ax2.bar(x, [y2[1][j]-y2[0][j] for j in range(len(y2[0]))], color='#83AF9B',width=0.5,label="avg",bottom=y2[0])
    ax2.bar(x, [y2[2][j]-y2[1][j] for j in range(len(y2[0]))], color='#FCB19A', width=0.5, label="max", bottom= y2[1])

    ax2.set_xlabel('项目规模大小-u∈[0.6，1.0]',size=20)
    ax2.set_ylabel('成本节省度（%）',size=20)
    # ax1.set_xticks()
    ax2.set_yticks([5,10,15,20,25,30])
    mp.legend(loc="best", fontsize=16)
    plt.savefig("./out_file/" + str(i) + "成本 u=1.png", dpi=800, bbox_inches='tight')
    plt.show()
pyplot3(ruba2, cost2, 3)