import datetime
import plotly as py
import plotly.figure_factory as ff

#Get the Gantt_chart

starttime=[0, 12, 2, 4, 35, 27, 42, 44, 55, 54, 67, 43, 64, 78, 53, 91]
finishtime=[0, 22, 12, 14, 37, 35, 48, 50, 59, 59, 72, 47, 69, 84, 63, 91]
du=[]
for i in range(len(starttime)):
      du.append(finishtime[i]-starttime[i])
print(du)
def Gantt_chart(start,finish):
      number_job=16
      initial_date = datetime.datetime.strptime("2019-01-01", "%Y-%m-%d")
      draw_list=[]
      start1=[]
      finish1=[]
      for i in range(number_job):
            start1.append(initial_date + datetime.timedelta(days=start[i]))
            finish1.append(initial_date + datetime.timedelta(days=finish[i]))
            draw_list.append({'Task':'活动'+str(i+1),"Start":start1[i],'Finish':finish1[i],"Complete":(100/number_job)*(i+1)})

      pyplt = py.offline.plot
      fig = ff.create_gantt(draw_list,  index_col='Complete', show_colorbar=True,height=1000,width=1200)
      pyplt(fig, filename='Gantt_chart.html')
Gantt_chart(starttime,finishtime)