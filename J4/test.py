
import time
import  random
Lead_time_E=[2,3,2,4,2,3,4]

start=time.time()
a=[1+Lead_time_E[i]*(0.6+0.3*random.random()) for i in range(len(Lead_time_E))]
end=time.time()
print(end-start)