


import Suppliers_MRCPSP
import GA_Suppliers_MRCPSP
def main(file):
    instance = Suppliers_MRCPSP.Instance()
    f_p = file
    f_CN = "./data/CNfks.xlsx"
    f_O = "./data/Ofs.xlsx"
    qfs = "./data/qfs.xlsx"
    n=0
    # M=[1, 3, 3, 3, 1, 3, 2, 3, 2, 2, 3, 2, 3, 2, 3, 1]
    # starttime=[0, 12, 2, 4, 35, 27, 42, 44, 55, 54, 67, 43, 64, 78, 53, 91]


    instance.loadData(file_project=f_p, file_CNfks=f_CN, file_Ofs=f_O, file_qfs=qfs)
    supplier=instance.initial_Supplier()

    for i in range(100):
        ind=GA_Suppliers_MRCPSP.GA_RCPSP_ruba(instance,100,supplier)
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

    doc=open("best.txt","w")
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

if __name__ == '__main__':
    main(file="./data/j141_8.mm")


