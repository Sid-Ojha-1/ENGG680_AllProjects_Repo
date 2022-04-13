#!/usr/bin/env python
# coding: utf-8

# #### <h1> <center> ENGG680 </center></h1>
# <h2> <center> Project (47 points)</center></h2>
# <center>
# <div class="alert alert-block alert-info">
# Due: Friday April 22 (midnight). To be submitted on D2L.
# </div></center>

# Edit this file and write your solutions to the problems in sections specified with `# Your solution goes here`. Test your code and when you were done, download this notebook as an `.ipynb` file and submit it to D2L. To get this file, in Jupyter notebook you can go to File -> Download as -> Notebook(.ipynb)

# # Accident Prediction
# The goal of this project is to get familiar with data wrangling and prepare a machine learning model to have an inital prediction by using real world data set.
# 
# Two data set of accident information of Calgary (Traffic_Incidents.csv) and (weather.csv) are given for this prediction.
# 

# ### Import Traffic_Incidents.csv and set START_DT in csv file as index (1 pts)

# In[1]:


# Your solution goes here
get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Traffic_Incidents.csv')
# print(data_frame)
df['START_DT'] = pd.to_datetime(df['START_DT'])
df.set_index("START_DT", inplace = True)
# print(data_frame.columns)


# ### Filter "INCIDENT INFO" (i.e. only keep ICIDENT INFO column and drop other columns from dataframe) (1 pts)

# In[2]:


# Your solution goes here
df.drop(df.loc[:, 'DESCRIPTION':'Point'].columns, axis = 1)  


# ### Check and drop null values from dataset if exist (1 pts)

# In[3]:


# Your solution goes here
df.dropna()


# ### plot daily accident counts (3 Pts)

# In[9]:


# Your solution goes here
df1 = df.groupby(df.index.date).count()
# df1 = df.groupby(df.index.date).resample('D').count()
df1['Count'].plot(figsize=(20, 10))
# df.reset_index().plot(x='START_DT', y='Count')


# ### plot weekly accident counts (3 Pts)

# In[24]:


# Your solution goes here
# df1 = df.groupby(df.index.date).resample('W').count()
df1 = df.resample('W').count()
# df2 = df1.groupby(df.index.date)

df1["Count"].plot(figsize = (20,10))
# df1['Count'].plot(figsize=(30, 10))


# ### plot the average traffic as a function of the time of the day and explain your observation ( 6 pts: 4 pts code + 2 pts your observation)

# In[10]:


# Your solution goes here


# ### Plot the average traffic to see how things change based on the day of the week and explain your observation ( 6 pts: 4 pts code + 2 pts your observation)

# In[11]:


# Your solution goes here


# ### plot the hourly trend between weekdays and weekends and explain your observation ( 8 pts: 6 pts code and 2 pts your observation)

# In[12]:


# Your solution goes here


# # Merging Datasets

# ### Load Daily weather data (weather.csv) (1 pts)

# In[13]:


# Your solution goes here


# ### Extract maximum/minimum temperature and drop Null values (1 pts)

# In[15]:


# Your solution goes here


# ### Add the following daily features and create your feature matrix: (10 pts)
# * X: Weekdays, average daily temperature
# * Y: Total number of accidents in that day

# In[ ]:


# Your solution goes here


# ### Create your model and use linearRegression class in sklearn for prediction (3 pts)

# In[ ]:


# Your solution goes here


# ### plot and compare your prediction with real accident data (3 pts)

# In[17]:


# Your solution goes here

