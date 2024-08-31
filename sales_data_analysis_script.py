import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import glob
import os

path = r"C:\Users\davngu\OneDrive - Leslie's Poolmart\Documents\David_Self_Improvement\Data_Project\Sales_Data_Analysis\datasets" # use your path
ext = r"*.csv"
all_files = glob.glob(os.path.join(path , ext))

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

frame["sale_date"] =  pd.to_datetime(frame["sale_time"]).dt.date 
frame["fiscal_sale_date"] =  pd.to_datetime(frame["sale_time"]).dt.date + pd.DateOffset(months=3)
frame["sale_time"] =  pd.to_datetime(frame["sale_time"]).dt.time
frame["fiscal_week"] = pd.to_datetime(frame['fiscal_sale_date']).dt.isocalendar().week
frame["fiscal_month"] = pd.to_datetime(frame['fiscal_sale_date']  ).dt.month 
frame["date"] = pd.to_datetime(frame['fiscal_sale_date']  ).dt.day
# frame["year"] = pd.to_datetime(frame['sale_date']).dt.year


frame.loc[ frame["purchaser_gender"]  == "male" , "gender_code"] = 1 
frame.loc[ frame["purchaser_gender"]  == "female" , "gender_code"] = 0

# print(frame)
###################################################################
#################Plot daily sales for all 50 weeks.################
###################################################################
frame_by_fweek = frame[["fiscal_sale_date","fiscal_week","fiscal_month"]]
frame_by_fweek = frame_by_fweek.groupby( by= ["fiscal_sale_date","fiscal_month","fiscal_week"] ).size().reset_index(name= 'sale_count_by_week')

plt.plot( frame_by_fweek["fiscal_week"] , frame_by_fweek["sale_count_by_week"]  )
##### the plot show from around week 30 - 35 have sale boom
##### let's investigate more about what date the sale is starting

#########################################################################################################################
################ It looks like there has been a sudden change in daily sales. What date did it occur? ###################
#########################################################################################################################
frame_by_fdate = frame[["fiscal_sale_date","fiscal_week"]]
frame_by_fdate["fiscal_week"].astype(int)
frame_by_fdate = frame_by_fdate[ (frame_by_fdate["fiscal_week"] <= 35) & (frame_by_fdate["fiscal_week"] >= 30) ]
frame_by_fdate = frame_by_fdate.groupby( by= ["fiscal_sale_date", "fiscal_week" ] ).size().reset_index(name= 'sale_by_date')
print(frame_by_fdate)
### the daily sale is sudden change at July 29 - fiscal date or April 29 as calendar date. 


##########################################################################################################################################
############ Is the change in daily sales at the date you selected statistically significant? If so, what is the p-value? ################
##########################################################################################################################################

rvs = frame_by_fdate["sale_by_date"]
stats.ttest_1samp(rvs, popmean= 732 )
### p-value of 732 is 2.135e-5, which is < 0.05. p-value of 732 is fall below significant level then it means statistically significant.    