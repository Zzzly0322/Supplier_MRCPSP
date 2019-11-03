# Author:Zhaofei
import linecache
import numpy as np
import pandas as pd
import  copy
import  matplotlib.pyplot as plt
import random
import Suppliers_MRCPSP
import  time


def fitness_cost(ins,ind_solution,supplier):
    fitness11 = ins.project_cost(ind_solution,supplier,ind_solution.R_order_time)
    fit=1/fitness11
    return fit

def fitness_ruba(ins,ind_solution,suppliers):
    fitness22 = ins.project_ruba(ind_solution,suppliers)
    return fitness22

def selected_p_cost(ins,pop_Suppliers,ind_solution):
    fitnesses = []
    be_ind=[]
    for supplier in pop_Suppliers:
        ind_solution.R_order_time = ins.initial_ordertime(ind_solution.starttime, ind_solution.M,supplier)
        fit= fitness_cost(ins,ind_solution,supplier)
        fitnesses.append(fit)
        copy_ind=copy.copy(ind_solution)
        be_ind.append(copy_ind)
    sum_fitnessre = sum(fitnesses)
    Min_cost=1/max(fitnesses)
    min_ind=be_ind[fitnesses.index(1/Min_cost)]
    min_sup=pop_Suppliers[fitnesses.index(1/Min_cost)]
    p_list_cost=[]


    for count in range(len(pop_Suppliers)):
        fit1= fitnesses[count]
        p_selected=fit1/sum_fitnessre
        p_list_cost.append(p_selected)


    return p_list_cost,Min_cost,min_ind,min_sup

def selected_p_ruba(ins,pop,suppliers):
    fitnesses = []
    for ind in pop:
        fit= fitness_ruba(ins,ind,suppliers)
        fitnesses.append(fit)
    sum_fitnessre = sum(fitnesses)
    MAX_ruba=max(fitnesses)
    max_ind_ruba=pop[fitnesses.index(MAX_ruba)]
    p_list_ruba=[]
    for ind in pop:
        fit1= fitness_ruba(ins,ind,suppliers)
        p_selected=fit1/sum_fitnessre
        p_list_ruba.append(p_selected)
    return p_list_ruba,max_ind_ruba,MAX_ruba

def mate_ruba(ins,pop,plist,pop_Supplier):
    new_offspring= []
    offspring_p_list = list(zip(pop, plist))
    for i in range(int(ins.popSize/2)):
        sum1_p = 0
        for ind1, p in offspring_p_list:
            sum1_p += p
            if random.random() < sum1_p: break
        child_order1 = ind1.order
        child_M1=ind1.M


        sum2_p = 0
        for ind2, p in offspring_p_list:
            sum2_p += p
            if random.random() < sum2_p: break
        child_order2 = ind2.order
        child_M2 = ind2.M


        #order
        if random.random() < ins.mate_pb:
            offspring_order1 = [0 for _ in range(len(child_order1))]
            offspring_order2 = [0 for _ in range(len(child_order2))]
            x = sorted(random.sample(range(len(child_order1)), 2))
            for i in range(x[0]):
                offspring_order1[i] = child_order1[i]
                offspring_order2[i] = child_order2[i]
            for j in range(x[1], len(child_order1)):
                offspring_order1[j] = child_order1[j]
                offspring_order2[j] = child_order2[j]
                pos1 = x[0]
                pos2 = x[0]
            for gene1 in child_order2:
                if gene1 not in offspring_order1:
                    offspring_order1[pos1] = gene1
                    pos1 += 1
            for gene2 in child_order1:
                if gene2 not in offspring_order2:
                    offspring_order2[pos2] = gene2
                    pos2 += 1

        else:
            offspring_order1 = child_order1
            offspring_order2 = child_order2
        #M
        if random.random() < ins.mate_pb:
            offspring_M1 = [0 for _ in range(len(child_order1))]
            offspring_M2 = [0 for _ in range(len(child_order2))]
            x = random.randint(1,15)
            for i in range(x):
                offspring_M1[i] = child_M1[i]
                offspring_M2[i] = child_M2[i]
            for j in range(x, len(child_M1)):
                offspring_M1[j] = child_M2[j]
                offspring_M2[j] = child_M1[j]

        else:
            offspring_M1 = child_M1
            offspring_M2 = child_M2

        #order time
        start_time1,finish_time1=ins.job_start_time(offspring_order1,offspring_M1)
        start_time2, finish_time2 = ins.job_start_time(offspring_order2, offspring_M2)
        offspring_order_time1=ins.initial_ordertime(start_time1,offspring_M1,pop_Supplier)
        offspring_order_time2 = ins.initial_ordertime(start_time2, offspring_M2, pop_Supplier)

        new_ind1=Suppliers_MRCPSP.Indivadul(offspring_order1,offspring_M1,start_time1,offspring_order_time1)
        new_ind2=Suppliers_MRCPSP.Indivadul(offspring_order2,offspring_M2,start_time2,offspring_order_time2)

        new_offspring.append(new_ind1)
        new_offspring.append(new_ind2)
    return new_offspring

def mate_cost(ins,pop_Suppliers,plist_cost):
    new_offspring = []
    offspring_p_list = list(zip(pop_Suppliers, plist_cost))
    for i in range(int(ins.popSize/2)):
        sum1_p = 0
        for ind1, p in offspring_p_list:
            rum = random.random()
            sum1_p += p
            if rum < sum1_p: break
        child1 = ind1
        sum2_p = 0
        for ind2, p in offspring_p_list:
            sum2_p += p
            if random.random() < sum2_p: break
        child2 = ind2
        if random.random() < ins.mate_pb:
            offspring1 = [0 for _ in range(len(child1))]
            offspring2 = [0 for _ in range(len(child2))]
            x = random.randint(2,len(child1)-1)
            for i in range(x):
                offspring1[i] = child1[i]
                offspring2[i] = child2[i]
            for j in range(x, len(child1)):
                offspring1[j] = child2[j]
                offspring2[j] = child1[j]

        else:
            offspring1 = child1
            offspring2 = child2
        new_offspring.append(offspring1)
        new_offspring.append(offspring2)
    return new_offspring

def mutate_ruba(ins,pop,pop_Supplier):

    offsprings=[]
    for ind in pop:
        if random.random()<ins.mutate_pb:
            move_job1 = random.choice(ind.order[1:14])
            ava_move_job = []
            order_copy = copy.copy(ind.order)
            index_pre = []
            for i in ins.job_predecessors[move_job1 - 1]:
                    index_pre.append(order_copy.index(i))
            premove_maxindex = max(index_pre)
            index_aft=[]
            for j in ins.job_successors[move_job1-1]:
                index_aft.append(order_copy.index(j))
            aftmove_minindex=min(index_aft)
            position=random.randint(premove_maxindex+1,aftmove_minindex-1)
            ind.order.insert(position,move_job1)
            if position<order_copy.index(move_job1):
                del ind.order[order_copy.index(move_job1)+1]
            else: del ind.order[order_copy.index(move_job1)]

            offspring_order=ind.order

            mutate_job=random.randint(1,15)
            while True:
                a=random.choice([1,2,3])
                if a!=ind.M[mutate_job]:
                    break
            ind.M[mutate_job]=a
            offspring_M=ind.M

            starttime,finishtime=ins.job_start_time(ind.order,ind.M)

            offspring_order_time = ins.initial_ordertime(starttime, offspring_M, pop_Supplier)

            offspring=Suppliers_MRCPSP.Indivadul(offspring_order,offspring_M,starttime,offspring_order_time)
            offsprings.append(offspring)
        else:
            offsprings.append(ind)


    return offsprings

def mutate_cost(ins,pop_Suppliers):

    offsprings=[]
    for ind in pop_Suppliers:
        if random.random()<ins.mutate_pb:
            move_re = random.randint(0,len(ind)-1)
            order_copy = copy.copy(ind)
            temp=[]
            count=1
            for j in ins.Ofs.loc["f"+str(move_re+1)]:
                if j!=0:
                    temp.append(count)
                count+=1
            while True:
                if  random.choice(temp)!=order_copy[move_re]:
                    order_copy[move_re]=random.choice(temp)
                    break
            offspring=order_copy
        else:
            offspring=ind
        offsprings.append(offspring)

    return offsprings

def GA_RCPSP_ruba(ins,NGEn,pop_Supplier):
    print(1)
    print("pop_Supplier",pop_Supplier)
    pop_inds=ins.initialSolution(pop_Supplier)
    min_ruba_list=[]
    current_best=pop_inds[0]
    for g in range(NGEn):
        print("--------ruba_Generation_%s-----------" % (g + 1))
        plist_ruba,max_ind_ruba,MAX_ruba=selected_p_ruba(ins,pop_inds,pop_Supplier)
        print(2)
        #mate
        offspring=mate_ruba(ins,pop_inds,plist_ruba,pop_Supplier)

        print(3)
        #mutate
        offspring=mutate_ruba(ins,offspring,pop_Supplier)

        print(4)

        pop_inds = offspring

        pop_inds.append(current_best)
        fits = []
        ruba=[]
        for ind in pop_inds:
            fit=fitness_ruba(ins,ind,pop_Supplier)
            fits.append(fit)
            ruba.append(1/fit)
        b = fits.index(max(fits))

        if max(fits)>fitness_ruba(ins,current_best,pop_Supplier):
            current_best=pop_inds[b]
        else:
            ruba.append(1/fitness_ruba(ins,current_best,pop_Supplier))

            pop_inds.append(current_best)

            # else:
            #     print("错误！！！！！！！！！！！！！！")

        # print("starrt_time",best_ind.starttime)

        print("Max_Fitness: %s" % max(fits))
        min_ruba=min(ruba)
        print("Min_time:", min_ruba)
        min_ruba_list.append(min_ruba)



    plt.plot(min_ruba_list)
    plt.ylabel("Min_cost")
    plt.xlabel("Generation")

    # plt.savefig("GA1", dpi=600)
    # plt.show()
    return  current_best


def GA_RCPSP_cost(ins,NGEn,ind_solution,m):
    print(1)
    min_cost_list=[]

    pop_Suppliers=[]
    for i in range(ins.popSize):
        pop_Suppliers.append(ins.initial_Supplier())
    print("pop_Supplier",pop_Suppliers)

    current_best_sup=pop_Suppliers[0]
    current_best_ind=ind_solution
    current_best=1/fitness_cost(ins,current_best_ind,current_best_sup)

    for g in range(NGEn):
        print("--------cost_eneration_%s-----------" % (g + 1))
        plist_cost,Min_cost,min_ind,min_sup=selected_p_cost(ins,pop_Suppliers,ind_solution)
        print(2)
        #mate
        offspring=mate_cost(ins,pop_Suppliers,plist_cost)
        print(3)
        #mutate
        offspring=mutate_cost(ins,offspring)
        print(4)
        pop_Suppliers=offspring

        if Min_cost<current_best:
            current_best_sup=min_sup
            current_best_ind=min_ind
            current_best=Min_cost

            cost=Min_cost
        else:
            cost=current_best
            pop_Suppliers[-1]=current_best_sup

        print("Min_cost:", cost)
        min_cost_list.append(cost)


    doc=open("solution.txt","a")
    print("\n", "-------------------%s次迭代------------------" % (m + 1), file=doc)
    print("min_cost_list", min_cost_list, file=doc)
    print("current_best_supplier",current_best_sup,file=doc)
    print("best_fit_cost",current_best,file=doc)
    print("-------------------------------------",file=doc)

    print("current_best.order",current_best_ind.order,file=doc)
    print("current_best.M",current_best_ind.M,file=doc)
    print("current_best.starttime",current_best_ind.starttime,file=doc)
    print("current_best.R_order_time",current_best_ind.R_order_time,file=doc)
    print("best_fit_ruba",fitness_ruba(ins,current_best_ind,current_best_sup),file=doc)

    doc.close()



    # if 1/fitness_cost(ins,ind_solution,current_best)< 1/fitness_cost(ins,ind_solution,ins.best_sup):
    ins.best_sup.append(current_best_sup)
    ins.best_ind.append(current_best_ind)
    ins.time.append(time.time())


    plt.plot(min_cost_list)
    plt.ylabel("Min_cost")
    plt.xlabel("Generation")

    # plt.savefig("GA1", dpi=600)
    # plt.show()





    return current_best_sup,current_best_ind


def Greedy_cost(ins,ind_solution):
    best_order_time = [["NaN" for i in range(6)] for _ in range(ins.number_job)]
    best_supplier=[]
    re_job=[[] for i in range(6)]
    total_cost=0
    totall_fix=0
    for re in range(6):
        order_time_temp = []
        print("--------------一次%s资源循环--------------------"%(re+1))
        for job in range(ins.number_job):
            if ins.job_model_resource[job+1][ind_solution.M[job]][2+re]!=0:
                re_job[re].append(job)
        # for t in range(ind_solution.starttime[-1]):
        re_job[re]=sorted(re_job[re], key=lambda x: ind_solution.starttime[x ])
        # candidate set
        S_temp = []
        count=1
        for j in ins.Ofs.loc["f" + str(re+1)]:
            if j != 0:
                S_temp.append(count)
            count+=1
        s_totall_cost = []
        for s in S_temp:
            order_time = [["NaN" for i in range(6)] for _ in range(ins.number_job)]
            print("--------------一次%s供应商循环--------------------" % (s))
            ordered_job=[0]
            time_order_count=[0 for _ in range(ind_solution.starttime[-1])]
            cost = 0
            for job in re_job[re]:
                print("--------------一次job-%s循环--------------------"%(job+1))
                single_fix_cost=ins.Ofs.loc["f" + str(re + 1)]["s"+str(s)]
                single_var_cost=0
                if ins.job_model_resource[job+1][ind_solution.M[job]][2+re]<= ins.k:
                    single_var_cost= ins.CNfks["S" + str(s )].loc["f" + str(re + 1)]["k1"]*ins.job_model_resource[job+1][ind_solution.M[job]][2+re]
                elif ins.k < ins.job_model_resource[job+1][ind_solution.M[job]][2+re] <= ins.kk:
                    single_var_cost= ins.CNfks["S" + str(s)].loc["f" + str(re+1)]["k2"]*ins.job_model_resource[job+1][ind_solution.M[job]][2+re]
                elif ins.job_model_resource[job+1][ind_solution.M[job]][2+re]  > ins.kk:
                    single_var_cost= ins.CNfks["S" + str(s)].loc["f" + str(re+1)]["k3"]*ins.job_model_resource[job+1][ind_solution.M[job]][2+re]

                single_order_time=ind_solution.starttime[job]-ins.Lead_time_E[s-1]
                # print("ins.job_model_resource[job+1][ind_solution.M[job]][2+re]",ins.job_model_resource[job+1][ind_solution.M[job]][2+re])
                # print("single_var_cost",single_var_cost)
                single_cost=single_fix_cost+single_var_cost

                muti_cost=1000
                muti_order_time=0
                inventory_cost=0
                muti_var_cost=0
                save_var_cost=0
                if ordered_job[-1]!=0 and order_time[ordered_job[-1]][re]!="NaN":
                    muti_order_time=order_time[ordered_job[-1]][re]
                    inventory_cost=ins.If[re]*(ind_solution.starttime[job]-muti_order_time-ins.Lead_time_E[s-1])
                    # print("job:",job,"st:",ind_solution.starttime[job],"order:",muti_order_time)
                    order_num=time_order_count[muti_order_time]+ ins.job_model_resource[job+1][ind_solution.M[job]][2+re]

                    if order_num <= ins.k:
                        muti_var_cost = ins.CNfks["S" + str(s)].loc["f" + str(re + 1)]["k1"]*ins.job_model_resource[job+1][ind_solution.M[job]][2+re]
                    elif ins.k < order_num <= ins.kk:
                        muti_var_cost = ins.CNfks["S" + str(s)].loc["f" + str(re+1)]["k2"]*ins.job_model_resource[job+1][ind_solution.M[job]][2+re]
                    elif order_num > ins.kk:
                        muti_var_cost = ins.CNfks["S" + str(s)].loc["f" + str(re+1)]["k3"]*ins.job_model_resource[job+1][ind_solution.M[job]][2+re]

                    save_var_cost=0
                    if time_order_count[muti_order_time] <= ins.k<order_num<=ins.kk:
                        save_var_cost = (ins.CNfks["S" + str(s)].loc["f" + str(re + 1)]["k1"]-ins.CNfks["S" + str(s)].loc["f" + str(re + 1)]["k2"]) * time_order_count[muti_order_time]
                    elif ins.k<time_order_count[muti_order_time] <= ins.kk<order_num:
                        save_var_cost = (ins.CNfks["S" + str(s)].loc["f" + str(re + 1)]["k2"]-ins.CNfks["S" + str(s)].loc["f" + str(re + 1)]["k3"]) * time_order_count[muti_order_time]
                    elif time_order_count[muti_order_time] <= ins.k < ins.kk < order_num:
                        save_var_cost = (ins.CNfks["S" + str(s)].loc["f" + str(re + 1)]["k1"] -ins.CNfks["S" + str(s)].loc["f" + str(re + 1)]["k3"]) * time_order_count[muti_order_time]

                    muti_cost=inventory_cost+muti_var_cost-save_var_cost


                if single_cost<muti_cost:
                    order_time[job][re]=single_order_time
                    time_order_count[single_order_time]+=ins.job_model_resource[job+1][ind_solution.M[job]][2+re]
                    cost+=single_cost
                if single_cost>muti_cost:
                    order_time[job][re]=muti_order_time
                    time_order_count[muti_order_time]+=ins.job_model_resource[job+1][ind_solution.M[job]][2+re]
                    cost+=inventory_cost+muti_var_cost-save_var_cost


                ordered_job.append(job)

                b=ins.order_inventory(ind_solution,re,s,order_time,ordered_job)


            copytime = order_time
            order_time_temp.append(copytime)

            a=copy.copy(cost)
            s_totall_cost.append(b)
            # print("cost:",cost)
        print("s_totall_cost",s_totall_cost)

        s_best_index=s_totall_cost.index(min(s_totall_cost))

        besttime=order_time_temp[s_best_index]

        for job in range(ins.number_job):
            for re in range(6):
                if besttime[job][re]!="NaN":
                    best_order_time[job][re]=besttime[job][re]


        best_supplier.append(S_temp[s_best_index])
        total_cost+=min(s_totall_cost)


    ind_solution.R_order_time=best_order_time
    print(best_supplier)
    print(total_cost)
    print(best_order_time)

    ins.best_ind.append(copy.copy(ind_solution))
    ins.best_sup.append(copy.copy(best_supplier))
    ins.time.append(time.time())



    return best_supplier,ind_solution

    # for re in  range(6):
    #     b=ins.order_inventory(ind_solution,re,best_supplier[re],best_order_time,re_job[re])
    #     total_cost111111111+=b
    #     print("b",b)
    # print("total_cost111111111",total_cost111111111)



    # ww=ins.project_cost1(ind_solution,best_supplier,best_order_time)
    # print(ww)


""" 
def ind_to_solution(ind,filename):
    duration,resourse_list,follow_nade=node_read(filename)
    #print(duration)
    #print(resourse_list)
    #print(follow_nade)
    schedule_node=[]
    resourse_limited=0
    start_time=0
    finish_time=[0 for i in range(33)]
    for i in ind:
        dura_time=duration[i]
        finish_time[i]=start_time+dura_time
"""
#ind_to_solution([1],"j301_1.sm")

# supplier= [1, 2, 5, 1, 7, 3]
# order= [1, 11, 8, 6, 2, 3, 4, 9, 13, 5, 10, 7, 14, 15, 12, 16]
# M =[1, 3, 2, 2, 3, 3, 3, 1, 2, 2, 2, 3, 2, 3, 1, 2]
# starttime =[0, 4, 16, 3, 22, 8, 26, 2, 4, 32, 4, 34, 0, 45, 57, 63]
# finishtime =[0, 14, 22, 12, 29, 16, 33, 4, 8, 37, 8, 43, 3, 53, 59, 63]
# duration =[0, 10, 6, 9, 7, 8, 7, 2, 4, 5, 4, 9, 3, 8, 2, 0]
# order_time =[['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], ['NaN', 1, 'NaN', 'NaN', 0, 0], [6, 'NaN', 6, 'NaN', 0, 'NaN'], ['NaN', 0, 0, 'NaN', 'NaN', 0], ['NaN', 19, 'NaN', 'NaN', 18, 20], [6, 'NaN', 6, 'NaN', 0, 'NaN'], [24, 'NaN', 'NaN', 24, 18, 'NaN'], [0, 'NaN', 0, 'NaN', 'NaN', 0], [2, 'NaN', 'NaN', 'NaN', 0, 0], [30, 'NaN', 'NaN', 30, 'NaN', 30], [2, 1, 'NaN', 0, 'NaN', 'NaN'], [32, 31, 'NaN', 32, 'NaN', 'NaN'], [-2, 'NaN', 'NaN', -2, 'NaN', 'NaN'], ['NaN', 31, 'NaN', 'NaN', 'NaN', 'NaN'], [55, 'NaN', 'NaN', 55, 53, 'NaN'], ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']]
#
# ind=Suppliers_MRCPSP.Indivadul(order,M,starttime,order_time)
# instance = Suppliers_MRCPSP.Instance()
# file="./data/j141_8.mm"
# f_p = file
# f_CN = "./data/CNfks.xlsx"
# f_O = "./data/Ofs.xlsx"
# qfs = "./data/qfs.xlsx"
# n = 0
#
# instance.loadData(file_project=f_p, file_CNfks=f_CN, file_Ofs=f_O, file_qfs=qfs)
#
# Greedy_cost(instance,ind)