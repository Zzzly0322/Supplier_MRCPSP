

import  copy
import Suppliers_MRCPSP
import GA_Suppliers_MRCPSP
import os

def main(file):
    instance = Suppliers_MRCPSP.Instance()

    file_temp = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    f_p = file
    f_CN = file_temp+"\data\CNfks.xlsx"
    f_O =file_temp+ "\data\Ofs.xlsx"
    qfs =file_temp+ "\data\qfs.xlsx"
    n=0
    # M=[1, 3, 3, 3, 1, 3, 2, 3, 2, 2, 3, 2, 3, 2, 3, 1]
    # starttime=[0, 12, 2, 4, 35, 27, 42, 44, 55, 54, 67, 43, 64, 78, 53, 91]

    doc = open("best.txt_%s" % ("J" + str(instance.number_job)), "w")
    instance.loadData(file_project=f_p, file_CNfks=f_CN, file_Ofs=f_O, file_qfs=qfs)
    supplier=instance.initial_Supplier()
    IRM=[]
    IC=[]
    ruba_com=[]
    cost_com=[]
    for z in range(5):
        instance.best_sup=[]
        instance.best_ind=[]
        for i in range(50):
            ind=GA_Suppliers_MRCPSP.GA_RCPSP_ruba(instance,50,supplier)
            # sup,ind=GA_Suppliers_MRCPSP.GA_RCPSP_cost(instance,1,ind,i)
            sup, ind = GA_Suppliers_MRCPSP.Greedy_cost(instance, ind)
            supplier=sup
        cost=[instance.project_cost(instance.best_ind[g],instance.best_sup[g],instance.best_ind[g].R_order_time) for g in range(len(instance.best_sup))]
        best_cost=min(cost)
        best_index=cost.index(best_cost)

        print(cost)


        best_S=instance.best_sup[best_index]
        best_I=instance.best_ind[best_index]
        ruba=instance.project_ruba(best_I,best_S)

        finishtime=[]
        duration=[]
        for i in range(len(best_I.M)):
            finishtime.append(best_I.starttime[i] + instance.job_model_duration[i + 1][best_I.M[i]])
            duration.append(instance.job_model_duration[i + 1][best_I.M[i]])


        doc=open("best.txt_%s"%("J"+str(instance.number_job)),"a")
        print("-------------------最终结果----------------------",file=doc)
        print("supplier",best_S,file=doc)
        print("order",best_I.order,file=doc)
        print("M",best_I.M, file=doc)
        print("starttime",best_I.starttime, file=doc)
        print("finishtime", finishtime, file=doc)
        print("duration", duration, file=doc)
        print("order_time",best_I.R_order_time, file=doc)
        best=instance.project_cost(best_I,best_S,best_I.R_order_time)
        print("best_cost",best,file=doc)
        print("best_ruba",ruba,file=doc)
        doc.close()


        e=copy.copy(ruba)
        t=copy.copy(best)

        IRM.append(e)
        IC.append(t)


        a, b, c, d = instance.job_start_time_2(best_I.order, best_I.M)
        best_I.starttime=a
        ordertime=instance.initial_ordertime(a,best_I.M,best_S)
        ruba_com.append(instance.project_ruba(best_I,best_S))
        cost_com.append(instance.project_cost(best_I,best_S,ordertime))

    print("\n")
    # print(IRM)
    # print(IC)
    # print("\n")
    #
    # print(ruba_com)
    # print(cost_com)



    IRM_rate=[(IRM[i]-ruba_com[i])/ruba_com[i] for i in range(len(IRM))]
    IC_rate = [( cost_com[i]- IC[i]) /  IC[i] for i in range(len(IC))]


    print(IRM_rate)
    print(IC_rate)

    print(max(IRM_rate),min(IRM_rate),sum(IRM_rate)/len(IRM))
    print(max(IC_rate), min(IC_rate), sum(IC_rate) / len(IC))

    doc.close()
if __name__ == '__main__':

    filename = "\data\j162_3.mm"
    file = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + filename
    main(file=file)


