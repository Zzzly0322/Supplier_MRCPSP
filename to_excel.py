


import pandas as pd

starttime =[0, 14, 4, 9, 19, 1, 28, 0, 2, 25, 14, 30, 0, 38, 50, 56]
finishtime =[0, 24, 14, 14, 21, 9, 30, 4, 8, 35, 19, 34, 5, 46, 55, 56]
def To_excel(starttime,finishtime):
    excel=[starttime,finishtime]
    datafram=pd.DataFrame(excel)
    datafram=datafram.T
    datafram.to_excel("print.xlsx")
    print(datafram)
To_excel(starttime,finishtime)
