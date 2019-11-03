


import data_read_MRCPSP
import pandas as pd
import random
import matplotlib.pyplot as plt
import  numpy as np
import  copy
import time
import random
class Indivadul():
    def __init__(self,order,M,starttime,R_order_time):
        self.order=order
        self.M=M
        self.starttime=starttime
        self.R_order_time=R_order_time
        # self.R_order_supplier=R_order_supplier


class Instance():
    def __init__(self):

        self.job_num_successors=[]
        self.job_predecessors = []
        self.job_successors=[]
        self.job_model_resource={1:{1:[0 for _ in range(8)],2:[0 for _ in range(8)],3:[0 for _ in range(8)]},32:{1:[0 for _ in range(8)],2:[0 for _ in range(8)],3:[0 for _ in range(8)]}}
        self.job_model_duration={1:{1:0,2:0,3:0},32:{1:0,2:0,3:0}}
        self.Lead_time_E=[2,3,2,4,2,3,4]
        self.Lead_time_0=[2.364793499419341, 3.590722183867771, 2.5540486141093632, 4.368226030629229, 2.316351827116401, 3.0796935154386236, 3.706033524317347]
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
        self.time=[]

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
                start_time[job - 1] = max(finish_time[pre_job - 1] for pre_job in self.job_predecessors[job - 1])+random.randint(0,4)
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
        # use_renewable_resource_1 = use_renewable_resource_1[:finish_time[self.number_job - 1]]
        # use_renewable_resource_2 = use_renewable_resource_2[:finish_time[self.number_job - 1]]




        solution_set.insert(0, 1)
        return start_time, finish_time

    def initial_Supplier(self):
        initial_supplier=[]
        for i in range(6):   #num of resource
            count=1
            temp=[]
            for j in self.Ofs.loc["f"+str(i+1)]:
                if j!=0:
                    temp.append(count)
                count+=1
            initial_supplier.append(random.choice(temp))
        return initial_supplier

    def initial_ordertime(self,starttime,model_set,pop_Supplier):
        re_list = []
        for resource_job in range(self.number_job):
            re_list.append(self.job_model_resource[resource_job + 1][model_set[resource_job]][2:])

        # choice_supplier_List=[["NaN" for i in range(len(re_list[0]))] for _ in range(self.number_job)]
        sorted_starttime_job = []
        start_temp = copy.copy(starttime)
        for i in range(self.number_job):
            min_job = start_temp.index(min(start_temp))
            sorted_starttime_job.append(min_job)
            start_temp[min_job] = 1000

        already_ordered = [0]
        order_time = [["NaN" for i in range(len(re_list[0]))] for _ in range(self.number_job)]
        for re_job in sorted_starttime_job:
            re_count = 0
            for resource_materials in re_list[re_job]:
                if resource_materials != 0:
                    if random.random() <= 0.5:
                        order_time[re_job][re_count] = starttime[re_job] - self.Lead_time_E[pop_Supplier[re_count] - 1]

                    else:
                        t_temp = [0]
                        for job_reed in already_ordered:
                            if order_time[job_reed][re_count] != "NaN":
                                t_temp.append(order_time[job_reed][re_count])

                        order_time[re_job][re_count] = min(max(t_temp),starttime[re_job] - self.Lead_time_E[pop_Supplier[re_count] - 1])
                re_count += 1
            already_ordered.append(re_job)
        return order_time

    def initialSolution(self,pop_Supplier):
        """
        initial the path
        :return: a adapative path
        """
        ind_list=[]
        for i in range(self.popSize):


            complete_set=[1]
            for w in range(self.number_job-1):
                ready_set = []
                for job in range(2,self.number_job+1):
                    if job not in complete_set:
                        if set(self.job_predecessors[job-1]).issubset(complete_set):
                            ready_set.append(job)
                if len(ready_set)!=0:
                    act_job=random.choice(ready_set)
                    complete_set.append(act_job)
            initial_set=complete_set
            model_set=[]
            [model_set.append(random.choice([1,2,3])) for i in range(self.number_job)]
            model_set[0]=1
            model_set[self.number_job-1]=1



            starttime,finishtime=self.job_start_time(initial_set,model_set)
            re_list=[]
            for resource_job in range(self.number_job):
                re_list.append(self.job_model_resource[resource_job+1][model_set[resource_job]][2:])

            # choice_supplier_List=[["NaN" for i in range(len(re_list[0]))] for _ in range(self.number_job)]
            sorted_starttime_job=[]
            start_temp=copy.copy(starttime)
            for i in range(self.number_job):
                min_job=start_temp.index(min(start_temp))
                sorted_starttime_job.append(min_job)
                start_temp[min_job]=1000

            already_ordered=[0]
            order_time= [["NaN" for i in range(len(re_list[0]))] for _ in range(self.number_job)]
            for re_job in sorted_starttime_job:
                re_count = 0
                for resource_materials in re_list[re_job]:
                    if resource_materials!=0:
                        # S_list = [i+1 for i, x in enumerate(self.Ofs.loc["f"+str(re_count+1)]) if x != 0]
                        # job_s=random.choice(S_list)
                        # choice_supplier_List[re_job][re_count]=job_s
                        if random.random()<=0.5:
                            order_time[re_job][re_count]=starttime[re_job]-self.Lead_time_E[pop_Supplier[re_count]-1]

                        else:
                            t_temp=[0]
                            for job_reed in already_ordered:
                                if order_time[job_reed][re_count]!="NaN":
                                    t_temp.append(order_time[job_reed][re_count])

                            order_time[re_job][re_count] =max(t_temp)
                    re_count+=1
                already_ordered.append(re_job)

            ind = Indivadul(order=initial_set,M=model_set,starttime=starttime,R_order_time=order_time)
            ind_list.append(ind)
            # print("order_time",order_time)
            # # print("choice_supplier_List",choice_supplier_List)
            # print("ind.M",ind.M)
            # print("ind.starttime",ind.starttime)
            # print("order",initial_set)
        return ind_list

    def project_quality(self,ind_solution):
        initial_supplier=self.initial_Supplier()
        Quality=1
        for job in range(self.number_job):
            # print(self.job_model_resource[job+1][ind_solution.M[job+1]])
            for job_res in self.job_model_resource[job+1][ind_solution.M[job]]:
                count = 1
                if job_res!=0:
                    Quality=Quality*self.qfs.loc["f"+str(count)]["s"+str(initial_supplier[count-1])]
                count+=1
        fitness_1=Quality
        return  fitness_1

    def project_ruba(self,ind_solution,suppliers):

        """
        注意job_re的取值
        :param ind_solution:
        :return:
        """
        ruba_totall=0
        delta_list = []
        for job in range(1,self.number_job-1):
            delta_temp=[]
            re_count=0
            for re in self.job_model_resource[job+1][ind_solution.M[job]][2:]:
                if re!=0:
                    s=suppliers[re_count]
                    a = self.Lead_time_0[s - 1]
                    delta_temp.append(a)
                re_count+= 1

            delta_i = max(delta_temp)
            ruba_totall += delta_i
            delta_list.append(delta_i)
            # delta_list.insert(0, 0)
            # delta_list.append(0)

        ls_list=[]
        for i in range(1,self.number_job-1):
            succ=[]
            for job in self.job_successors[i]:
                succ.append(ind_solution.starttime[job-1])
            success_min=min(succ)
            ls_list.append(success_min)
        ruba=0

        for i in range(2,self.number_job):

            ruba+=(delta_list[i-2]/ruba_totall)*(ls_list[i-2]-ind_solution.starttime[i-1])
        fitness_2=ruba
        return fitness_2

    # def project_cost(self,ind_solution,supplier):
    #     order_cost=0
    #     # renewable_resource_cost=0
    #     # time_cost=0
    #     inventory_cost=0
    #
    #     temp_list=[[[0 for _ in range(7)]for f in   range(6)] for t in range(ind_solution.starttime[-1]+10)]
    #     #需要负数的时间   t f s
    #     order_fixed_cost=0
    #     order_per_cost=0
    #
    #     re_time = [[] for r in range(6)]
    #     for resource in range(6):
    #         for job in range(self.number_job):
    #             if self.job_model_resource[job + 1][ind_solution.M[job]][2 + resource] != 0:
    #                 if ind_solution.R_order_time[job][resource] not in re_time[resource]:
    #                     order_fixed_cost += self.Ofs.loc["f" + str(resource + 1)]["s" + str(supplier[resource])]
    #                     re_time[resource].append(ind_solution.R_order_time[job][resource])
    #
    #     # print(order_fixed_cost)
    #     for job in range(self.number_job):
    #         count_f=0
    #         for time in  ind_solution.R_order_time[job]:
    #             if time !="NaN":
    #                 s=supplier[count_f]
    #                 temp_list[time-1+10][count_f][s-1]+=self.job_model_resource[job+1][ind_solution.M[job]][2+count_f]
    #             count_f+=1
    #
    #
    #
    #     for tt in range(len(temp_list)):
    #         for ff in range(len(temp_list[0])):
    #             for ss in range(len(temp_list[0][0])):
    #                 if temp_list[tt][ff][ss]!=0:
    #                     if temp_list[tt][ff][ss]<=self.k:
    #                         order_per_cost+=self.CNfks["S"+str(ss+1)].loc["f"+str(ff+1)]["k1"]*temp_list[tt][ff][ss]
    #                     elif self.k<temp_list[tt][ff][ss]<=self.kk:
    #                         order_per_cost+=self.CNfks["S"+str(ss+1)].loc["f"+str(ff+1)]["k2"]*temp_list[tt][ff][ss]
    #                     elif temp_list[tt][ff][ss]>self.kk :
    #                         order_per_cost+=self.CNfks["S"+str(ss+1)].loc["f"+str(ff+1)]["k3"]*temp_list[tt][ff][ss]
    #
    #     order_cost=order_per_cost+order_fixed_cost
    #     # print("------------ordercost",order_cost)
    #
    #     #库存成本
    #     for job in range(self.number_job):
    #         count_f3=0
    #         # print(ind_solution.R_order_time)
    #         for f3_time in ind_solution.R_order_time[job]:
    #             if f3_time!="NaN":
    #                 D_value=ind_solution.starttime[job]-f3_time-self.Lead_time_E[supplier[count_f3]-1]
    #                 # print("-------Dvalue",D_value)
    #                 inventory_cost+=D_value*self.If[count_f3]
    #             count_f3+=1
    #     print("------------inventorycost", inventory_cost)
    #     print("------------fix",order_fixed_cost)
    #     #延误成本
    #
    #     delay_cost=ind_solution.starttime[-1]*10
    #
    #     fitnesses3=inventory_cost+order_cost+delay_cost
    #     return fitnesses3


    def order_inventory(self,ind_solution,resource,supplier,ordertime,ordered_job):

        temp_list=[0 for t in range(ind_solution.starttime[-1]+10)]
        #需要负数的时间   t f s
        order_fixed_cost=0
        order_per_cost=0
        re_time = []
        for job in ordered_job:
            if self.job_model_resource[job + 1][ind_solution.M[job]][2 + resource] != 0:
                if ordertime[job][resource] not in re_time:
                    order_fixed_cost += self.Ofs.loc["f" + str(resource + 1)]["s" + str(supplier)]
                    re_time.append(ordertime[job][resource])
        # print("order_fixed_cost ",order_fixed_cost )

        for job in ordered_job:
            time=ordertime[job][resource]
            if time !="NaN":
                temp_list[time-1+10]+=self.job_model_resource[job+1][ind_solution.M[job]][2+resource]
        # print(temp_list)
        for count  in temp_list:
            if count!=0:
                if count<=self.k:
                    order_per_cost+=self.CNfks["S"+str(supplier)].loc["f"+str(resource+1)]["k1"]*count
                elif self.k<count<=self.kk:
                    order_per_cost+=self.CNfks["S"+str(supplier)].loc["f"+str(resource+1)]["k2"]*count
                elif count>self.kk :
                    order_per_cost+=self.CNfks["S"+str(supplier)].loc["f"+str(resource+1)]["k3"]*count

        # print("order_per_cost",order_per_cost)
        inventory_cost=0

        for job in ordered_job:
            f3_time=ordertime[job][resource]
            if f3_time!="NaN":
                D_value=ind_solution.starttime[job]-f3_time-self.Lead_time_E[supplier-1]
                # print("-------Dvalue",D_value)
                inventory_cost+=D_value*self.If[resource]
        #         print("D_value",D_value)
        # print("inventory_cost",inventory_cost)
        n=order_fixed_cost + order_per_cost+inventory_cost
        return n

    def project_cost(self,ind_solution,supplier,ordertime):
        totall_cost=0
        for re in range(6):
            re_job=[[] for i in range(6)]
            # print("--------------一次%s资源循环--------------------" % (re + 1))
            for job in range(self.number_job):
                if self.job_model_resource[job + 1][ind_solution.M[job]][2 + re] != 0:
                    re_job[re].append(job)
            # for t in range(ind_solution.starttime[-1]):
            re_job[re] = sorted(re_job[re], key=lambda x: ind_solution.starttime[x])

            supp=supplier[re]
            cost=self.order_inventory(ind_solution,re,supp,ordertime,re_job[re])
            copy_cost=copy.copy(cost)
            totall_cost+=copy_cost

            # print(re,"资源：",cost)
        return totall_cost

    def job_start_time_2(self, solution_set, solution_model):

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
# order= [1, 5, 3, 8, 4, 2, 9, 6, 13, 11, 7, 10, 14, 12, 15, 16]
# M =[1, 2, 3, 3, 1, 2, 1, 3, 3, 1, 3, 1, 1, 3, 3, 1]
# starttime =[0, 13, 3, 4, 0, 23, 28, 2, 3, 30, 4, 34, 2, 36, 48, 61]
# finishtime =[0, 23, 13, 14, 2, 28, 30, 8, 9, 32, 9, 38, 4, 44, 58, 61]
# duration= [0, 10, 10, 10, 2, 5, 2, 6, 6, 2, 5, 4, 2, 8, 10, 0]
# order_time= [['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], [11, 'NaN', 1, 'NaN', 'NaN', 11], [0, 'NaN', 'NaN', 0, 0, 'NaN'], ['NaN', 1, 'NaN', 'NaN', 0, 0], [-2, 'NaN', -3, -2, 'NaN', 'NaN'], ['NaN', 20, 'NaN', 'NaN', 0, 21], [26, 'NaN', 'NaN', 26, 'NaN', 21], ['NaN', -1, 'NaN', 0, 'NaN', 0], [1, 'NaN', 'NaN', 0, 0, 'NaN'], [26, 'NaN', 27, 'NaN', 'NaN', 28], ['NaN', 1, 1, 'NaN', 'NaN', 2], ['NaN', 20, 'NaN', 26, 'NaN', 32], [0, 'NaN', -1, 'NaN', 'NaN', 0], ['NaN', 20, 'NaN', 'NaN', 'NaN', 'NaN'], [46, 'NaN', 'NaN', 46, 'NaN', 46], ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']]
# ind=Indivadul(order,M,starttime,order_time)
#
# instance =Instance()
# file="./data/j141_8.mm"
# f_p = file
# f_CN = "./data/CNfks.xlsx"
# f_O = "./data/Ofs.xlsx"
# qfs = "./data/qfs.xlsx"
# n = 0
# # M=[1, 3, 3, 3, 1, 3, 2, 3, 2, 2, 3, 2, 3, 2, 3, 1]
# # starttime=[0, 12, 2, 4, 35, 27, 42, 44, 55, 54, 67, 43, 64, 78, 53, 91]
#
#
# instance.loadData(file_project=f_p, file_CNfks=f_CN, file_Ofs=f_O, file_qfs=qfs)
#
#
# ordertime=[['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], [-2, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], [-2, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], ['NaN', -2, 'NaN', 'NaN', 'NaN', 'NaN'], [-2, 'NaN', -4, 'NaN', 'NaN', 'NaN'], ['NaN', 19, 'NaN', 'NaN', 'NaN', 'NaN'], [26, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], ['NaN', -2, 'NaN', 'NaN', 'NaN', 'NaN'], [-2, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], [26, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], ['NaN', -2, 'NaN', 'NaN', 'NaN', 'NaN'], ['NaN', 19, 'NaN', 'NaN', 'NaN', 'NaN'], [-2, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], ['NaN', 19, 'NaN', 'NaN', 'NaN', 'NaN'], [26, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']]
# re=2
# s=4
#
# b=instance.order_inventory(ind,re,s,ordertime,[4])
# print(b)

# instance=Instance()
# f_p="./data/j141_8.mm"
# f_CN="./data/CNfks.xlsx"
# f_O="./data/Ofs.xlsx"
# qfs="./data/qfs.xlsx"
#
# instance.loadData(file_project=f_p,file_CNfks=f_CN,file_Ofs=f_O,file_qfs=qfs)
#
#
# # instance.project_quality(pop[0])
# a=instance.initial_Supplier()
# print(a)
# pop=instance.initialSolution(a)