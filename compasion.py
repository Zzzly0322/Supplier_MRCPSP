
import  random
import  pandas as pd
import  data_read_MRCPSP

import matplotlib.pylab as plt  # 导入绘图包
import matplotlib.pyplot as mp
from pylab import *  # 图像中的title,xlabel,ylabel均使用中文
import numpy as np
import matplotlib.font_manager
class Instance():
    def __init__(self):

        self.job_num_successors=[]
        self.job_predecessors = []
        self.job_successors=[]
        self.job_model_resource={1:{1:[0 for _ in range(8)],2:[0 for _ in range(8)],3:[0 for _ in range(8)]},16:{1:[0 for _ in range(8)],2:[0 for _ in range(8)],3:[0 for _ in range(8)]}}
        self.job_model_duration={1:{1:0,2:0,3:0},16:{1:0,2:0,3:0}}
        self.Lead_time_E=[2,3,2,4,2,3,4]
        self.Lead_time_0 = [1.596287439804636, 1.2806260440591148, 1.5897067275742427, 1.091564721558271,1.3053531642763252, 1.385663738387799, 1.498642774983689]
        self.resource_capacity=[]
        self.number_job =None
        self.number_renewable_resources = None
        self.number_unrenewable_resources = None
        self.resource_capacity = None
        self.upper_bound=228
        self.CNfks={}
        self.Ofs=None
        self.qfs=None
        self.popSize=100
        self.k=4
        self.kk=8
        self.If=[1,3,2,4,3,2]
        self.choice_supplier=[]
        self.order_time=[]
        self.mate_pb=0.8
        self.mutate_pb=0.1


        self.best_ind=[]
        self.best_sup=[]

    def loadData(self,file_project,file_CNfks,file_Ofs,file_qfs):
        data_read_MRCPSP.dataStore(self, file_project)
        data_read_MRCPSP.read_CNfks(self,file_CNfks)
        data_read_MRCPSP.read_Ofs(self,file_Ofs)
        data_read_MRCPSP.read_qfs(self,file_qfs)

    def job_start_time(self, solution_set, solution_model):

        scheduled_list = [1]
        start_time = [0 for _ in range(self.number_job)]
        finish_time = [0 for _ in range(self.number_job)]
        use_renewable_resource_1 = [0 for i in range(self.upper_bound)]
        use_renewable_resource_2 = [0 for i in range(self.upper_bound)]
        solution_set.remove(1)
        for job in solution_set:
            if set(self.job_predecessors[job - 1]).issubset(scheduled_list):
                start_time[job - 1] = max(finish_time[pre_job - 1] for pre_job in self.job_predecessors[job - 1] )
                finish_time[job - 1] = start_time[job - 1] + self.job_model_duration[job][solution_model[job - 1]]
                while True:
                    count = 0
                    for i in range(self.job_model_duration[job][solution_model[job - 1]]):

                        if self.job_model_resource[job][solution_model[job - 1]][0] + use_renewable_resource_1[start_time[job - 1] + i] < self.resource_capacity[0] and \
                                self.job_model_resource[job][solution_model[job - 1]][1] + use_renewable_resource_2[start_time[job - 1] + i] < self.resource_capacity[1]:
                            count += 1
                    if count == self.job_model_duration[job][solution_model[job - 1]]:
                        for duration in range(start_time[job - 1], start_time[job - 1] + self.job_model_duration[job][solution_model[job - 1]]):
                            use_renewable_resource_1[duration] += self.job_model_resource[job][solution_model[job - 1]][0]
                            use_renewable_resource_2[duration] += self.job_model_resource[job][solution_model[job - 1]][1]
                        scheduled_list.append(job)
                        break
                    else:
                        start_time[job - 1] += 1
                        finish_time[job - 1] += 1
            else:
                print("Solution Order Error !")
                print(self.job_predecessors[job - 1], scheduled_list)
        use_renewable_resource_1 = use_renewable_resource_1[:finish_time[self.number_job - 1]]
        use_renewable_resource_2 = use_renewable_resource_2[:finish_time[self.number_job - 1]]




        solution_set.insert(0, 1)
        return start_time, finish_time,use_renewable_resource_1,use_renewable_resource_2

    def resource(self, start_time,solution_model):
        use_renewable_resource_1 = [0 for i in range(self.upper_bound)]
        use_renewable_resource_2 = [0 for i in range(self.upper_bound)]
        for job in range(1,len(start_time)+1):
            for duration in range(start_time[job - 1], start_time[job - 1] + self.job_model_duration[job][solution_model[job - 1]]):
                use_renewable_resource_1[duration] += self.job_model_resource[job][solution_model[job - 1]][0]
                use_renewable_resource_2[duration] += self.job_model_resource[job][solution_model[job - 1]][1]

        use_renewable_resource_1 = use_renewable_resource_1[:start_time[self.number_job - 1]]
        use_renewable_resource_2 = use_renewable_resource_2[:start_time[self.number_job - 1]]





        return use_renewable_resource_1,use_renewable_resource_2


    def inventory_consump(self,starttime,finishtime,ordertime,model,S):

        inventory = [[0 for _ in range(starttime[-1])] for i in range(6)]
        for re in range(6):
            for t in range(len(inventory[re])):
                In=0
                out=0
                for job in range(self.number_job):
                    if  ordertime[job][re] ==t-self.Lead_time_E[S[re]-1]:
                        In+=self.job_model_resource[job + 1][model[job]][re + 2]
                        # print(job+1,"re",re,"In:",In)
                print("t",t, "re", re, "In:", In)
                for job in range(self.number_job):
                    if starttime[job]<t<=finishtime[job]:
                        out+=self.job_model_resource[job + 1][model[job]][re + 2]/self.job_model_duration[job + 1][model[job]]
                inventory[re][t]=round(inventory[re][t-1]+In-out,2)
                # if inventory[re][t]<0.1:
                #     inventory[re][t]=0
        for i in range(6):
            print(inventory[i])
        return inventory

    def pylot(self,inven):

        x = [i+1 for i in range(len(inven[0]))]
        y0 =  inven[0]
        y1 = inven[1]
        y2 = inven[2]
        y3 = inven[3]
        y4 = inven[4]
        y5 = inven[5]
        y=[y0,y1,y2,y3,y4,y5]
        # y4 = [0, 4, 7, 11, 8, 10, 9, 8, 10, 13, 8, 14, 11, 16, 18, 18]
        # y5 = [0, 4, 5, 11, 9, 10, 9, 8, 11, 13, 9, 19, 11, 16, 18, 19]
        # y6 = [0, 4, 5, 11, 10, 10, 10, 6, 12, 13, 13, 19, 11, 16, 18, 19]
        # y7 = [0, 4, 5, 11, 11, 10, 11, 6, 13, 13, 11, 15, 11, 16, 18, 18]
        # y8 = [0, 4, 5, 11, 12, 8, 8, 6, 12, 14, 12, 19, 11, 17, 19, 19]


        matplotlib.rcParams["font.family"] = "Kaiti"
        matplotlib.rcParams["font.size"] = 20

        # z=[[[y1[i]-y[i]] for i in range(len(y))], [[y2[i]-y[i]] for i in range(len(y))],[[y3[i]-y[i]] for i in range(len(y))],[[y4[i]-y[i]] for i in range(len(y))], [[y5[i]-y[i]] for i in range(len(y))],[[y6[i]-y[i]] for i in range(len(y))], [[y7[i]-y[i]] for i in range(len(y))], [[y8[i]-y[i]] for i in range(len(y))]]
        # for i in z:
        #     a.append(sum(i)/19)

        mp.gcf().set_facecolor(np.ones(3) * 240 / 255)  # 设置背景色


        #
        #
        #   # 绘制折线图像1,圆形点，标签，线宽
        #
        #

        if True:
            fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
            ax1.plot(x, y0, '-.', c='#030303', label='资源-"0"', linewidth=1)  # 绘制折线图像1,圆形点，标签，线宽
            mp.legend(loc=1, fontsize=8)
            ax1.set_xlabel('时间', size=16)
            ax1.set_ylabel('库存状态', size=16)
            ax1.set_xticks(range(0,len(x),2))

            plt.tick_params(labelsize=10)
            labels = ax1.get_xticklabels() + ax1.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]

            # # ax2.set_ylabel('y2', fontproperties=myfont,size=18)
            # 自动适应刻度线密度，包括x轴，y轴
            # fig.autofmt_xdate()
            plt.savefig("./out_file/res1.png", dpi=600, bbox_inches='tight',transparent=True )
            plt.show()
        if True:
            fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
            ax1.plot(x, y1, '*-.', c='#FF8C00', label='资源-"1"', linewidth=1)
            mp.legend(loc=1, fontsize=8)
            ax1.set_xlabel('时间', size=16)
            ax1.set_ylabel('库存状态', size=16)
            ax1.set_xticks(range(0, len(x), 2))

            plt.tick_params(labelsize=10)
            labels = ax1.get_xticklabels() + ax1.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]

            # # ax2.set_ylabel('y2', fontproperties=myfont,size=18)
            # 自动适应刻度线密度，包括x轴，y轴
            # fig.autofmt_xdate()
            plt.savefig("./out_file/res2.png", dpi=600, bbox_inches='tight', transparent=True)
            plt.show()
        if True:
            fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
            ax1.plot(x, y2, 'd--', c='r', label='资源-"2"', linewidth=1)
            mp.legend(loc=1, fontsize=8)
            ax1.set_xlabel('时间', size=16)
            ax1.set_ylabel('库存状态', size=16)
            ax1.set_xticks(range(0, len(x), 2))

            plt.tick_params(labelsize=10)
            labels = ax1.get_xticklabels() + ax1.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]

            # # ax2.set_ylabel('y2', fontproperties=myfont,size=18)
            # 自动适应刻度线密度，包括x轴，y轴
            # fig.autofmt_xdate()
            plt.savefig("./out_file/res3.png", dpi=600, bbox_inches='tight', transparent=True)
            plt.show()
        if True:
            fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
            ax1.plot(x, y3, 'v:', c='b', label='资源-"3"', linewidth=1)
            mp.legend(loc=1, fontsize=8)
            ax1.set_xlabel('时间', size=16)
            ax1.set_ylabel('库存状态', size=16)
            ax1.set_xticks(range(0, len(x), 2))

            plt.tick_params(labelsize=10)
            labels = ax1.get_xticklabels() + ax1.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]

            # # ax2.set_ylabel('y2', fontproperties=myfont,size=18)
            # 自动适应刻度线密度，包括x轴，y轴
            # fig.autofmt_xdate()
            plt.savefig("./out_file/res4.png", dpi=600, bbox_inches='tight', transparent=True)
            plt.show()
        if True:
            fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
            ax1.plot(x, y4, '*-.', c='#8968CD', label='资源-"4"', linewidth=1)
            mp.legend(loc=1, fontsize=8)
            ax1.set_xlabel('时间', size=16)
            ax1.set_ylabel('库存状态', size=16)
            ax1.set_xticks(range(0, len(x), 2))

            plt.tick_params(labelsize=10)
            labels = ax1.get_xticklabels() + ax1.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]

            # # ax2.set_ylabel('y2', fontproperties=myfont,size=18)
            # 自动适应刻度线密度，包括x轴，y轴
            # fig.autofmt_xdate()
            plt.savefig("./out_file/res5.png", dpi=600, bbox_inches='tight', transparent=True)
            plt.show()
        if True:
            fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
            ax1.plot(x, y5, 'd--', c='#8B4726', label='资源-"5"', linewidth=1)
            mp.legend(loc=1, fontsize=8)
            ax1.set_xlabel('时间', size=16)
            ax1.set_ylabel('库存状态', size=16)
            ax1.set_xticks(range(0, len(x), 2))

            plt.tick_params(labelsize=10)
            labels = ax1.get_xticklabels() + ax1.get_yticklabels()
            [label.set_fontname('Times New Roman') for label in labels]

            # # ax2.set_ylabel('y2', fontproperties=myfont,size=18)
            # 自动适应刻度线密度，包括x轴，y轴
            # fig.autofmt_xdate()
            plt.savefig("./out_file/res6.png", dpi=600, bbox_inches='tight', transparent=True)
            plt.show()


    def ruba_com(self,buffer1,buffer2,M,suppliers):
        ruba_totall=0
        delta_list = []
        for job in range(self.number_job):
            delta_temp=[0]
            re_count=0
            for re in self.job_model_resource[job+1][M[job]][2:]:
                if re!=0:
                    s=suppliers[re_count]
                    a = self.Lead_time_0[s - 1]
                    delta_temp.append(a)
                re_count+= 1

            delta_i = max(delta_temp)
            ruba_totall += delta_i
            delta_list.append(delta_i)
        ind_ruba_origin=0
        ind_ruba_comp=0
        for i in range(self.number_job):
            ind_ruba_origin+=buffer1[i]*delta_list[i]
            ind_ruba_comp += buffer2[i] * delta_list[i]

        print("ind_ruba_origin",ind_ruba_origin)
        print("ind_ruba_comp",ind_ruba_comp)
        print((ind_ruba_origin-ind_ruba_comp)/ind_ruba_comp)


ins=Instance()

f_p = "./data/j141_8.mm"
f_CN = "./data/CNfks.xlsx"
f_O = "./data/Ofs.xlsx"
qfs = "./data/qfs.xlsx"

ins.loadData(file_project=f_p, file_CNfks=f_CN, file_Ofs=f_O, file_qfs=qfs)
"""
order=[1, 3, 6, 2, 4, 13, 9, 8, 11, 5, 7, 10, 14, 12, 15, 16]
M=[1, 2, 3, 1, 1, 3, 1, 2, 3, 3, 3, 1, 3, 3, 2, 1]
a,b,c,d=ins.job_start_time(order,M)
e=[c,d]
data=pd.DataFrame(e)
data.to_excel("renewable.xlsx")
print(a)
print(b)
print(c)
print(d)
"""
"""
starttime=[0, 14, 4, 9, 19, 1, 28, 0, 2, 25, 14, 30, 0, 38, 50, 56]
M=[1, 2, 3, 1, 1, 3, 1, 2, 3, 3, 3, 1, 3, 3, 2, 1]
r1,r2=ins.resource(starttime,M)
e=[r1,r2]
data=pd.DataFrame(e)
data.to_excel("renewable_comp.xlsx")
print(r1)
print(r2)
"""

supplier =[1, 2, 5, 7, 6, 3]
order= [1, 6, 13, 11, 9, 3, 8, 2, 4, 5, 10, 14, 15, 7, 12, 16]
M =[1, 2, 1, 3, 3, 2, 2, 3, 3, 3, 1, 3, 3, 3, 3, 1]
starttime= [0, 14, 3, 3, 13, 3, 27, 8, 3, 24, 1, 37, 2, 35, 47, 61]
finishtime= [0, 24, 8, 13, 20, 8, 33, 14, 9, 34, 3, 46, 7, 43, 57, 61]
duration= [0, 10, 5, 10, 7, 5, 6, 6, 6, 10, 2, 9, 5, 8, 10, 0]
order_time= [['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], [-1, 'NaN', -1, 'NaN', 'NaN', 11], [-1, 0, 'NaN', -1, 'NaN', 'NaN'], ['NaN', 0, 'NaN', 'NaN', -2, 1], ['NaN', 10, 'NaN', 'NaN', -2, 11], ['NaN', 0, 'NaN', 'NaN', -2, 1], ['NaN', 21, 'NaN', 'NaN', 21, 22], ['NaN', 0, 'NaN', -1, 'NaN', 1], [-1, 'NaN', 'NaN', -1, -2, 'NaN'], ['NaN', 21, 'NaN', 'NaN', 21, 22], [-1, 'NaN', -1, 'NaN', -2, 'NaN'], [35, 32, 'NaN', 33, 'NaN', 'NaN'], [-1, 'NaN', -1, 'NaN', -2, 'NaN'], ['NaN', 32, 'NaN', 'NaN', 'NaN', 'NaN'], [35, 'NaN', 'NaN', 33, 'NaN', 45], ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']]

# for job in range(16):
#     if order_time[job][1]!='NaN':
#         print("job","M","re","ordertime","st","ft")
#         print(job+1,M[job],ins.job_model_resource[job+1][M[job]][3],order_time[job][1],starttime[job],finishtime[job])

# inven=ins.inventory_consump(starttime,finishtime,order_time,M,supplier)
#
# ins.pylot(inven)

buffer1=[0,3,5,9,4,0,4,23,26,1,0,11,40,4,0,0]
buffer2=[0,0,5,7,0,0,0,16,21,0,4,9,30,0,0,0]
suppliers=[1,2,5,7,6,3]

ins.ruba_com(buffer1,buffer2,M,suppliers)

# a,b,c,d=ins.job_start_time(order,M)
# print(a)
# print(b)
# print(c)
# print(d)
#
# e=[c,d]
# data=pd.DataFrame(e)
# data.to_excel("renewable_comp.xlsx")
#
#
# a,b=ins.resource(starttime,M)
# e=[a,b]
# data=pd.DataFrame(e)
# data.to_excel("renewable.xlsx")