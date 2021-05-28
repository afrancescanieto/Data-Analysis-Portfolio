#!/usr/bin/env python
# coding: utf-8

# # Portfolio Analysis
# #### Adrian Nieto Manzanares

# ## What to expect: 
# 
# In these three portfolio analysis' you can expect a couple of things to help decide whether which stocks are best
# for your bank account and retirement plan. 
# 1. **A 15 year view of each stocks' market value.** 
#     - This particular analysis point is essential because it can give you a rough estimate of the consistency in 
#         decisions each company has. Being young allows for more risky investment decisions, but unfortuantly the older we 
#         get the less time we have to get money making seeing things in the long term alot more secure. 
# 2. **A 15 year overview of the volume of each stock throughout the years**
#     - People who have more experience with investing with stock tend to be more tactful in making decisions on whether or not           to invest in a company. Seeing the 15 year course how many people have invested in each company can help create smarter         decsions on whether or not to invest in a risky low volume stock or a high volume high payback stock.
# 3. **Percentage of Mututal Funds Holders of each stock**
#     - By seeing how many of the shareholders are investing in mutual fund, it allows you to make a calculated decision on               whether or not to diversify through ownership. Since not all investments perform well at the same time, having
#         diversification allows you to take advantage of the potential of the best ones and offset the impact of the poorly   
#         performaced investments. 
#     
# _Below you can find a small portion of the code that belongs to each of these points_
#     
# | **Key Points** |       Code        |
# |-----------------|:-------------|
# |  A 15 year view of each stocks' market value  |  ``'Adj Close':'PFE Final'``|
# |-----------------+--------------+
# |  A 15 year overview of the volume of each stock throughout the years    |     ``plt.title('Pfizer Inc. \n15 Year Volume')``         |
# |-----------------+--------------+
# |   Percentage of Mututal Funds Holders of each stock    |   ``pfemutualfunds = pd.read_html``           |
# 

# ## Pharmaceutical  Industry Stock Portfolio
# 

# In[1]:


import pandas as pd # import for all pandas data 
import matplotlib.pyplot as plt # Imports for simple plotting 
from matplotlib import style # Import graph style 
# import numpy as np # Import numpy to create an array 
from statistics import mean
#import quandl # importing data from quandl package 
import datetime
import pickle # activates pickle into the program 
import pandas_datareader as web


# In[2]:


style.use('fivethirtyeight') # Declaring First style 


# In[3]:


start = datetime.datetime(2005,1,1) # Start Date for ALL of the portfolio dataframes
end = datetime.datetime.now() # End date for ALL of the portfolio dataframes 


# In[4]:


# I wasn't able to use quandl due to the particular subscription I have but this would be the api_key code to help 
# Encrypt the data
# api_key = open('quandlapikey.txt','r').read()  


# ## Pfizer Inc. General Data 

# In[5]:


# variables used for general pickling and datframe appending 
# a non-defined benchmark
df_Pfizer = web.DataReader("PFE", "yahoo", start, end )
df_Pfizer.rename(columns={'Adj Close':'PFE Final'}, inplace=True)


# In[6]:


# if we were allowed to attach files to the finalexam this the set up for using the .csv file
# query = "EOD/PFE"
# df_Pfizer = quandl.get(query,start_date="2000-01-01",authtoken=api_key)  # here we are loading the data of the Pfizer stock from quandl
# print(df_Pfizer.head())

def grab_initial_pfe_data(): # defined function containing the dataframe declarations and pickling 
    
    main_df = pd.DataFrame() # empty dataframe that is used as a placeholder // will be used for pickling 
    
    # Specific stock dataframe 
    df_Pfizer = web.DataReader("PFE", "yahoo", start, end )
    df_Pfizer.rename(columns={'Adj Close':'PFE Final'}, inplace=True)
    
    # if:else statement for ensuring that the previously empty dataframe is filled 
    if main_df.empty:
        main_df = df_Pfizer
    else:
        main_df = main_df.join(df_Pfizer)
    
    # one way to go about pickling the data for joining stock data in the future 
    pickle_out = open('PFE_data.pickle','wb') # writing in the pickle data
    pickle.dump(main_df, pickle_out) # manually dumping it in 
    pickle_out.close() # closing
    
grab_initial_pfe_data() # calling the previouly declared function 


# In[7]:



PFE_Data = pd.read_pickle('PFE_data.pickle') # read in pickle data 
print(PFE_Data)


# pickle_in = open('PFE_data.pickle','rb')
# PFE_Data = pickle.load(pickle_in)
# pickle_in.close()


# In[8]:


PFE_Data[['High','Low','Open','Close','PFE Final']].plot() # plotting specific variables of the dataframe 
plt.xlabel('Year') # changing the label of the x axis 
plt.ylabel('Stock Price') # changing the label of the y axis 
plt.title('Pfizer Inc.\n15 Year Market Value') # changing the plot title 
plt.legend(markerfirst=False) # changing the legend positioning 
plt.rcParams['lines.linewidth'] = 0.5 # changing the marker width 
plt.show() # show the plot 


# In[9]:


PFE_Data[['Volume']].plot()
plt.xlabel('Year')
plt.ylabel('Num of Shares')
plt.title('Pfizer Inc. \n15 Year Volume')
plt.legend().remove() # removing the legend from the data since it is self explanatory 
plt.subplots_adjust(left=0.12, bottom=0.20, right=0.93, top=0.90, wspace=0.2, hspace=0) # adjust graph size
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[10]:


def grab_initial_pfe_data():
    
    main_df = pd.DataFrame()
    
    df_Pfizer = web.DataReader("PFE", "yahoo", start, end )
    df_Pfizer.rename(columns={'Adj Close':'PFE Final'}, inplace=True)
    PFE_pct_change = df_Pfizer.pct_change() # applying percent change formula to the entire dataframe and all of its variables
    PFE_pct_change.dropna(how='all',inplace=True) # dropping the NaNs
    # you can also ffill or bfillor replace the value, but i this context I found it best to drop them 
    
    if main_df.empty:
        main_df = PFE_pct_change
    else:
        main_df = main_df.join(PFE_pct_change)
    
    pickle_out = open('PFE_data_ptp.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_pfe_data()


# In[11]:


PFE_Data_pct= pd.read_pickle('PFE_data_ptp.pickle')
print(PFE_Data_pct.head())


# In[12]:



PFE_Data_pct[['High','Low','Open','Close','PFE Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Pfizer Inc. \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[13]:


PFE_Data_pct= pd.read_pickle('PFE_data_ptp.pickle') # reading in the pickle of Pct Change 
PFE_Data_Correlation = PFE_Data_pct.corr() # Creating a Correlation Table of the Percent Change 
print(PFE_Data_Correlation.describe()) # Describing all of the Correlation  


# In[14]:


resample_PFE = PFE_Data_pct.resample('M').mean() #  resampling the data by month using the mean 
print(resample_PFE.head())


# In[15]:


plt.style.use('ggplot') # change of graph style 
resample_PFE[['High','Low','Open','Close','PFE Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Pfizer Inc. \nResampled Percent Change By Month')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[16]:



def grab_initial_pfe_data():
    
    
    main_df = pd.DataFrame()
    
    df_Pfizer = web.DataReader("PFE", "yahoo", start, end )
    df_Pfizer.rename(columns={'Adj Close':'PFE Final'}, inplace=True)
    
    #usuage of the single point percent change formula on the adjusted closing variable of the dataframe 
    df_Pfizer['PFE Final'] = (df_Pfizer['PFE Final']-df_Pfizer['PFE Final'][0]) / df_Pfizer['PFE Final'][0] * 100.0

    df_Pfizer.dropna(how='all',inplace=True) # dropping the NaNs


    if main_df.empty:
        main_df = df_Pfizer
    else:
        main_df = main_df.join(df_Pfizer)
    
    pickle_out = open('PFE_data_singlep.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_pfe_data()


# In[17]:


PFE_Data_pct_single= pd.read_pickle('PFE_data_singlep.pickle')
print(PFE_Data_pct_single.head())


# In[18]:


plt.style.use('classic')
PFE_Data_pct_single= pd.read_pickle('PFE_data_singlep.pickle')
PFE_Data_pct_single[['PFE Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Pfizer Inc. Adjusted Final Closing Prices \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[19]:


PFE_Data_pct_single= pd.read_pickle('PFE_data_singlep.pickle')
PFE_Final_Correlation = PFE_Data_pct_single.corr()
print(PFE_Final_Correlation['PFE Final'].describe())


# In[20]:


PFE_Data_pct_single= pd.read_pickle('PFE_data_singlep.pickle') 
PFE_Data_pct_single['PFE Final Mean'] = PFE_Data_pct_single['PFE Final'].rolling(window=12).mean() 
# applying the rolling mean to the percent change data to see the average throughout a 10 month period 
PFE_Data_pct_single['PFE Final STD'] = PFE_Data_pct_single['PFE Final'].rolling(window=12).std() 
# applying the rolling standard deviation to the percent change data to see the std throughout a 10 month period 


# In[21]:


print(PFE_Data_pct_single[['PFE Final','PFE Final Mean']])


# In[22]:


# this just helps split and organize the information into 2 graphs making it more readable 
fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

PFE_Data_pct_single['PFE Final'].plot(ax=ax1)
PFE_Data_pct_single['PFE Final Mean'].plot(ax=ax1)
PFE_Data_pct_single['PFE Final STD'].plot(ax=ax2)

plt.title('PFE Final Adjusted 10 month Rolling Standard Deviation and Mean')

plt.show()


# In[23]:


pfemutualfunds = pd.read_html('https://money.cnn.com/quote/shareholders/shareholders.html?symb=PFE&subView=institutional')
print(pfemutualfunds) # getting mutual fund percentage data from website


# In[24]:


print(pfemutualfunds[2])# finding a specific dataframe and bring it to light


# # Johnson & Johnson General Data

# In[25]:


# query = "EOD/JNJ"
# df_JNJ = quandl.get(query, trim_start="2000-01-01", authtoken=api_key)
# print(df_JNJ.head())


# In[26]:



df_Johnson = web.DataReader("JNJ", "yahoo", start, end )
df_Johnson.rename(columns={'Adj Close':'JNJ Final'}, inplace=True)


# In[27]:




def grab_initial_jnj_data():
    
    main_df = pd.DataFrame()
    
    df_Johnson = web.DataReader("JNJ", "yahoo", start, end )
    df_Johnson.rename(columns={'Adj Close':'JNJ Final'}, inplace=True)
    
    if main_df.empty:
        main_df = df_Johnson
    else:
        main_df = main_df.join(df_Johnson)
    
    pickle_out = open('JNJ_data.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_jnj_data()


# In[28]:



JNJ_Data = pd.read_pickle('JNJ_data.pickle')
print(JNJ_Data)


# In[29]:


JNJ_Data[['High','Low','Open','Close','JNJ Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Johnson & Johnson \n10 Year Market Value')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[30]:


JNJ_Data[['Volume']].plot()
plt.xlabel('Year')
plt.ylabel('Num of Shares')
plt.title('Johnson & Johnson Inc. \n15 Year Volume')
plt.legend().remove()
plt.subplots_adjust(left=0.12, bottom=0.20, right=0.93, top=0.90, wspace=0.2, hspace=0) # adjust graph size
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[31]:


def grab_initial_jnj_data():
    
    main_df = pd.DataFrame()
    
    df_Johnson = web.DataReader("JNJ", "yahoo", start, end )
    df_Johnson.rename(columns={'Adj Close':'JNJ Final'}, inplace=True)
    JNJ_pct_change = df_Johnson.pct_change()
    JNJ_pct_change.dropna(how='all',inplace=True) 
    
    if main_df.empty:
        main_df = JNJ_pct_change
    else:
        main_df = main_df.join(JNJ_pct_change)
    
    pickle_out = open('JNJ_data_ptp.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_jnj_data()


# In[32]:


JNJ_Data_pct= pd.read_pickle('JNJ_data_ptp.pickle')
print(JNJ_Data_pct.head())


# In[33]:



JNJ_Data_pct[['High','Low','Open','Close','JNJ Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Johnson & Johnson\n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[34]:


JNJ_Data_pct= pd.read_pickle('JNJ_data_ptp.pickle')
JNJ_Data_Correlation = JNJ_Data_pct.corr()
print(JNJ_Data_Correlation.describe())


# In[35]:


resample_JNJ = JNJ_Data_pct.resample('M').mean() # how = 'mean'
print(resample_JNJ.head())


# In[36]:


plt.style.use('ggplot')
resample_JNJ[['High','Low','Open','Close','JNJ Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Johnson & Johnson\nResampled Percent Change By Month')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[37]:



def grab_initial_jnj_data():
    
    
    main_df = pd.DataFrame()
    
    df_Johnson = web.DataReader("JNJ", "yahoo", start, end )
    df_Johnson.rename(columns={'Adj Close':'JNJ Final'}, inplace=True)
    
    df_Johnson['JNJ Final'] = (df_Johnson['JNJ Final']-df_Johnson['JNJ Final'][0]) / df_Johnson['JNJ Final'][0] * 100.0

    df_Johnson.dropna(how='all',inplace=True) 


    if main_df.empty:
        main_df = df_Johnson
    else:
        main_df = main_df.join(df_Johnson)
    
    pickle_out = open('JNJ_data_singlep.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_jnj_data()


# In[38]:


JNJ_Data_pct_single= pd.read_pickle('JNJ_data_singlep.pickle')
print(JNJ_Data_pct_single.head())


# In[39]:


plt.style.use('classic')
JNJ_Data_pct_single= pd.read_pickle('JNJ_data_singlep.pickle')
JNJ_Data_pct_single[['JNJ Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Johnson& Johnson Adjusted Final Closing Prices \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[40]:


JNJ_Data_pct_single= pd.read_pickle('JNJ_data_singlep.pickle')
JNJ_Final_Correlation = JNJ_Data_pct_single.corr()
print(JNJ_Final_Correlation['JNJ Final'].describe())


# In[41]:


JNJ_Data_pct_single= pd.read_pickle('JNJ_data_singlep.pickle')
JNJ_Data_pct_single['JNJ Final Mean'] = JNJ_Data_pct_single['JNJ Final'].rolling(window=12).mean()
JNJ_Data_pct_single['JNJ Final STD'] = JNJ_Data_pct_single['JNJ Final'].rolling(window=12).std() 


# In[42]:


print(JNJ_Data_pct_single[['JNJ Final','JNJ Final Mean']])


# In[43]:


fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

JNJ_Data_pct_single['JNJ Final'].plot(ax=ax1)
JNJ_Data_pct_single['JNJ Final Mean'].plot(ax=ax1)
JNJ_Data_pct_single['JNJ Final STD'].plot(ax=ax2)

plt.title('JNJ Final Adjusted 10 month Rolling Standard Deviation and Mean')

plt.show()


# In[44]:


jnjmutualfunds = pd.read_html('https://money.cnn.com/quote/shareholders/shareholders.html?symb=JNJ&subView=institutional')
print(jnjmutualfunds) # getting mutual fund percentage data from website


# In[45]:


print(jnjmutualfunds[2])# finding a specific dataframe and bring it to light


# # Merck & Company Inc. General Data 

# In[46]:


df_Merck = web.DataReader("MRK", "yahoo", start, end )
df_Merck.rename(columns={'Adj Close':'MRK Final'}, inplace=True)


# In[47]:


# query = "EOD/MRK"
# df_Merck = quandl.get(query,start_date="2000-01-01",authtoken=api_key)  # here we are loading the data of the Merck stock from quandl
# print(df_Merck.head())

def grab_initial_mrk_data():
    
    main_df = pd.DataFrame()
    
    df_Merck = web.DataReader("MRK", "yahoo", start, end )
    df_Merck.rename(columns={'Adj Close':'MRK Final'}, inplace=True)
    
    if main_df.empty:
        main_df = df_Merck
    else:
        main_df = main_df.join(df_Merck)
    
    pickle_out = open('MRK_data.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_mrk_data()


# In[48]:


MRK_Data = pd.read_pickle('MRK_data.pickle')
print(MRK_Data)


# In[49]:


MRK_Data[['High','Low','Open','Close','MRK Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')

plt.title('Merck & Company Inc.\n15 Year Market Value')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[50]:


MRK_Data[['Volume']].plot()
plt.xlabel('Year')
plt.ylabel('Num of Shares')
plt.title('Merck & Company Inc. \n15 Year Volume')
plt.legend().remove()
plt.subplots_adjust(left=0.12, bottom=0.20, right=0.93, top=0.90, wspace=0.2, hspace=0) # adjust graph size
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[51]:


def grab_initial_mrk_data():
    
    main_df = pd.DataFrame()
    
    df_Merck = web.DataReader("MRK", "yahoo", start, end )
    df_Merck.rename(columns={'Adj Close':'MRK Final'}, inplace=True)
    MRK_pct_change = df_Merck.pct_change()
    MRK_pct_change.dropna(how='all',inplace=True) 
    
    if main_df.empty:
        main_df = MRK_pct_change
    else:
        main_df = main_df.join(MRK_pct_change)
    
    pickle_out = open('MRK_data_ptp.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_mrk_data()


# In[52]:


MRK_Data_pct= pd.read_pickle('MRK_data_ptp.pickle')
print(MRK_Data_pct.head())


# In[53]:


MRK_Data_pct[['High','Low','Open','Close','MRK Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Merck & Company Inc. \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[54]:


MRK_Data_pct= pd.read_pickle('MRK_data_ptp.pickle')
MRK_Data_Correlation = MRK_Data_pct.corr()
print(MRK_Data_Correlation.describe())


# In[55]:


resample_MRK = MRK_Data_pct.resample('M').mean() # how = 'mean'
print(resample_MRK.head())


# In[56]:


plt.style.use('ggplot')
resample_MRK[['High','Low','Open','Close','MRK Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Merck & Company Inc. \nResampled Percent Change By Month')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[57]:


def grab_initial_mrk_data():
    
    
    main_df = pd.DataFrame()
    
    df_Merck = web.DataReader("MRK", "yahoo", start, end )
    df_Merck.rename(columns={'Adj Close':'MRK Final'}, inplace=True)
    
    df_Merck['MRK Final'] = (df_Merck['MRK Final']-df_Merck['MRK Final'][0]) / df_Merck['MRK Final'][0] * 100.0

    df_Merck.dropna(how='all',inplace=True) 


    if main_df.empty:
        main_df = df_Merck
    else:
        main_df = main_df.join(df_Merck)
    
    pickle_out = open('MRK_data_singlep.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_mrk_data()


# In[58]:


MRK_Data_pct_single= pd.read_pickle('MRK_data_singlep.pickle')
print(MRK_Data_pct_single.head())


# In[59]:


plt.style.use('classic')
MRK_Data_pct_single= pd.read_pickle('MRK_data_singlep.pickle')
MRK_Data_pct_single[['MRK Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Merck & Company Inc. Adjusted Final Closing Prices \n10 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[60]:


MRK_Data_pct_single= pd.read_pickle('MRK_data_singlep.pickle')
MRK_Final_Correlation = MRK_Data_pct_single.corr()
print(MRK_Final_Correlation['MRK Final'].describe())


# In[61]:


MRK_Data_pct_single= pd.read_pickle('MRK_data_singlep.pickle')
MRK_Data_pct_single['MRK Final Mean'] = MRK_Data_pct_single['MRK Final'].rolling(window=12).mean()
MRK_Data_pct_single['MRK Final STD'] = MRK_Data_pct_single['MRK Final'].rolling(window=12).std() 


# In[62]:


print(MRK_Data_pct_single[['MRK Final','MRK Final Mean']])


# In[63]:


fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

MRK_Data_pct_single['MRK Final'].plot(ax=ax1)
MRK_Data_pct_single['MRK Final Mean'].plot(ax=ax1)
MRK_Data_pct_single['MRK Final STD'].plot(ax=ax2)

plt.title('MRK Final Adjusted 10 month Rolling Standard Deviation and Mean')

plt.show()


# In[64]:


mrkmutualfunds = pd.read_html('https://money.cnn.com/quote/shareholders/shareholders.html?symb=MRK&subView=institutional')
print(mrkmutualfunds) # getting mutual fund percentage data from website


# In[65]:


print(mrkmutualfunds[2])# finding a specific dataframe and bring it to light


# ## Gathering all the data from the Three Stocks 

# In[66]:


# gathering the data from each stock pickle into a usable dataframe 
Pfizer_df = pd.read_pickle('PFE_data.pickle') 
Johnson_df = pd.read_pickle('JNJ_data.pickle')
Merck_df = pd.read_pickle('MRK_data.pickle')


All_Raw_Stock = pd.DataFrame() # empty dataframe place holder for the appending of the 3 dataframes 
All_Raw_Stock_Pharm = All_Raw_Stock.append([Pfizer_df,Johnson_df,Merck_df]) # appendment of the 3 dataframes 
# could also concat in which it would be  
# ALL_Stock_Concat = pd.concat([Pfizer_df,Johnson_df,Merck_df])
All_Raw_Stock_Pharm = All_Raw_Stock_Pharm.drop(["High","Low","Open","Close"], axis=1) 
# dropping non-essential columns for analysis 


# In[67]:


print(All_Raw_Stock_Pharm)


# In[68]:


All_Raw_Stock_Pharm.to_pickle('All_Raw_Stock_Pharm.pickle')


# In[69]:


All_Raw_Stock_Pharm = pd.read_pickle('All_Raw_Stock_Pharm.pickle')
All_Raw_Pharm_p2p = All_Raw_Stock_Pharm.pct_change() 
# calculating the percent change of all the adjusted closing prices 


# In[70]:


print(All_Raw_Pharm_p2p.head())


# In[71]:


All_Raw_Pharm_p2p.dropna(inplace=True)
print(All_Raw_Pharm_p2p.head())


# In[72]:


plt.style.use('default')
All_Raw_Pharm_p2p[['PFE Final','JNJ Final','MRK Final']].plot()
              
plt.legend()
plt.show()


# In[73]:


plt.style.use('grayscale')
All_Raw_Pharm_p2p[['Volume']].plot()
plt.legend()
plt.ylabel('# of Shares by Millions')
plt.show()


# In[74]:


All_Raw_Pharm_p2p.to_pickle('All_Raw_Pharm_p2p.pickle')


# In[75]:


# All_Raw_Stock_Pharm = pd.read_pickle('All_Raw_Stock_Pharm.pickle')

# Below we have a rolling apply function and execution 
# I did not include it in the code as I didn't see it necessary and the significant amount of NaNs made it useless
# uncomment to see it work. 
# def moving_average(values):
#     val = mean(values) + 1
#     return val

# All_Raw_Stock_Pharm['Rolling Volume'] = All_Raw_Stock_Pharm['Volume'].rolling(50).apply(moving_average, raw=True)

# plt.style.use('classic')
# All_Raw_Stock_Pharm[['Rolling Volume','Volume']].plot()
# plt.legend()
# plt.ylabel('# of Shares by Millions')
# plt.show()


# # Entertainment Stock Portfolio 

# ## The Walt Disney Company General Data

# In[76]:


style.use('fivethirtyeight')


# In[77]:


df_Disney = web.DataReader("DIS", "yahoo", start, end )
df_Disney.rename(columns={'Adj Close':'DIS Final'}, inplace=True)


# In[78]:


def grab_initial_dis_data():
    
    main_df = pd.DataFrame()
    
    df_Disney = web.DataReader("DIS", "yahoo", start, end )
    df_Disney.rename(columns={'Adj Close':'DIS Final'}, inplace=True)
    
    if main_df.empty:
        main_df = df_Disney
    else:
        main_df = main_df.join(df_Disney)
    
    pickle_out = open('DIS_data.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_dis_data()


# In[79]:


DIS_Data = pd.read_pickle('DIS_data.pickle')
print(DIS_Data)


# pickle_in = open('DIS_data.pickle','rb')
# DIS_Data = pickle.load(pickle_in)
# pickle_in.close()


# In[80]:


DIS_Data[['High','Low','Open','Close','DIS Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('The Walt Disney Company  \n15 Year Market Value')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[81]:


DIS_Data[['Volume']].plot()
plt.xlabel('Year')
plt.ylabel('Num of Shares')
plt.title('The Walt Disney Company \n15 Year Volume')
plt.legend().remove()
plt.subplots_adjust(left=0.12, bottom=0.20, right=0.93, top=0.90, wspace=0.2, hspace=0) # adjust graph size
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[82]:


def grab_initial_dis_data():
    
    main_df = pd.DataFrame()
    
    df_Disney = web.DataReader("DIS", "yahoo", start, end )
    df_Disney.rename(columns={'Adj Close':'DIS Final'}, inplace=True)
    DIS_pct_change = df_Disney.pct_change()
    DIS_pct_change.dropna(how='all',inplace=True) 
    
    if main_df.empty:
        main_df = DIS_pct_change
    else:
        main_df = main_df.join(DIS_pct_change)
    
    pickle_out = open('DIS_data_ptp.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_dis_data()


# In[83]:


DIS_Data_pct= pd.read_pickle('DIS_data_ptp.pickle')
print(DIS_Data_pct.head())


# In[84]:


DIS_Data_pct[['High','Low','Open','Close','DIS Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('The Walt Disney Company \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[85]:


DIS_Data_pct= pd.read_pickle('DIS_data_ptp.pickle')
DIS_Data_Correlation = DIS_Data_pct.corr()
print(DIS_Data_Correlation.describe())


# In[86]:


resample_DIS = DIS_Data_pct.resample('M').mean() # how = 'mean'
print(resample_DIS.head())


# In[87]:


plt.style.use('ggplot')
resample_DIS[['High','Low','Open','Close','DIS Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('The Walt Disney Company \nResampled Percent Change By Month')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[88]:


def grab_initial_dis_data():
    
    
    main_df = pd.DataFrame()
    
    df_Disney = web.DataReader("DIS", "yahoo", start, end )
    df_Disney.rename(columns={'Adj Close':'DIS Final'}, inplace=True)
    
    df_Disney['DIS Final'] = (df_Disney['DIS Final']-df_Disney['DIS Final'][0]) / df_Disney['DIS Final'][0] * 100.0

    df_Disney.dropna(how='all',inplace=True) 


    if main_df.empty:
        main_df = df_Disney
    else:
        main_df = main_df.join(df_Disney)
    
    pickle_out = open('DIS_data_singlep.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_dis_data()


# In[89]:


DIS_Data_pct_single= pd.read_pickle('DIS_data_singlep.pickle')
print(DIS_Data_pct_single.head())


# In[90]:


plt.style.use('classic')
DIS_Data_pct_single= pd.read_pickle('DIS_data_singlep.pickle')
DIS_Data_pct_single[['DIS Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('The Walt Disney Company Adjusted Final Closing Prices \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[91]:


DIS_Data_pct_single= pd.read_pickle('DIS_data_singlep.pickle')
DIS_Final_Correlation = DIS_Data_pct_single.corr()
print(DIS_Final_Correlation['DIS Final'].describe())


# In[92]:


DIS_Data_pct_single= pd.read_pickle('DIS_data_singlep.pickle')
DIS_Data_pct_single['DIS Final Mean'] = DIS_Data_pct_single['DIS Final'].rolling(window=12).mean()
DIS_Data_pct_single['DIS Final STD'] = DIS_Data_pct_single['DIS Final'].rolling(window=12).std() 


# In[93]:


print(DIS_Data_pct_single[['DIS Final','DIS Final Mean']])


# In[94]:


fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

DIS_Data_pct_single['DIS Final'].plot(ax=ax1)
DIS_Data_pct_single['DIS Final Mean'].plot(ax=ax1)
DIS_Data_pct_single['DIS Final STD'].plot(ax=ax2)

plt.title('DIS Final Adjusted 10 month Rolling Standard Deviation and Mean')

plt.show()


# In[95]:


dismutualfunds= pd.read_html('https://money.cnn.com/quote/shareholders/shareholders.html?symb=DIS&subView=institutional')
print(dismutualfunds) # getting mutual fund percentage data from website


# In[96]:


print(dismutualfunds[2])# findinga specific dataframe and bring it to light


# ## Netflix General Data

# In[97]:


style.use('fivethirtyeight')


# In[98]:


df_Netflix = web.DataReader("NFLX", "yahoo", start, end )
df_Netflix.rename(columns={'Adj Close':'NFLX Final'}, inplace=True)


# In[99]:


def grab_initial_nflx_data():
    
    main_df = pd.DataFrame()
    
    df_Netflix = web.DataReader("NFLX", "yahoo", start, end )
    df_Netflix.rename(columns={'Adj Close':'NFLX Final'}, inplace=True)
    
    if main_df.empty:
        main_df = df_Netflix
    else:
        main_df = main_df.join(df_Netflix)
    
    pickle_out = open('NFLX_data.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_nflx_data()


# In[100]:


NFLX_Data = pd.read_pickle('NFLX_data.pickle')
print(NFLX_Data)


# In[101]:


NFLX_Data[['High','Low','Open','Close','NFLX Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Netflix, Inc.\n15 Year Market Value')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[102]:


NFLX_Data[['Volume']].plot()
plt.xlabel('Year')
plt.ylabel('Num of Shares')
plt.title('Netflix, Inc. \n10 Year Volume')
plt.legend().remove()
plt.subplots_adjust(left=0.12, bottom=0.20, right=0.93, top=0.90, wspace=0.2, hspace=0) # adjust graph size
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[103]:


def grab_initial_nflx_data():
    
    main_df = pd.DataFrame()
    
    df_Netflix = web.DataReader("NFLX", "yahoo", start, end )
    df_Netflix.rename(columns={'Adj Close':'NFLX Final'}, inplace=True)
    NFLX_pct_change = df_Netflix.pct_change()
    NFLX_pct_change.dropna(how='all',inplace=True) 
    
    if main_df.empty:
        main_df = NFLX_pct_change
    else:
        main_df = main_df.join(NFLX_pct_change)
    
    pickle_out = open('NFLX_data_ptp.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_nflx_data()


# In[104]:


NFLX_Data_pct= pd.read_pickle('NFLX_data_ptp.pickle')
print(NFLX_Data_pct.head())


# In[105]:


NFLX_Data_pct[['High','Low','Open','Close','NFLX Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Netflix, Inc. \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[106]:


NFLX_Data_pct= pd.read_pickle('NFLX_data_ptp.pickle')
NFLX_Data_Correlation = NFLX_Data_pct.corr()
print(NFLX_Data_Correlation.describe())


# In[107]:


resample_NFLX = NFLX_Data_pct.resample('M').mean() # how = 'mean'
print(resample_NFLX.head())


# In[108]:


plt.style.use('ggplot')
resample_NFLX[['High','Low','Open','Close','NFLX Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Netflix, Inc. \nResampled Percent Change By Month')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[109]:


def grab_initial_nflx_data():
    
    
    main_df = pd.DataFrame()
    
    df_Netflix = web.DataReader("NFLX", "yahoo", start, end )
    df_Netflix.rename(columns={'Adj Close':'NFLX Final'}, inplace=True)
    
    df_Netflix['NFLX Final'] = (df_Netflix['NFLX Final']-df_Netflix['NFLX Final'][0]) / df_Netflix['NFLX Final'][0] * 100.0

    df_Netflix.dropna(how='all',inplace=True) 


    if main_df.empty:
        main_df = df_Netflix
    else:
        main_df = main_df.join(df_Netflix)
    
    pickle_out = open('NFLX_data_singlep.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_nflx_data()


# In[110]:


NFLX_Data_pct_single= pd.read_pickle('NFLX_data_singlep.pickle')
print(NFLX_Data_pct_single.head())


# In[111]:


plt.style.use('classic')
NFLX_Data_pct_single= pd.read_pickle('NFLX_data_singlep.pickle')
NFLX_Data_pct_single[['NFLX Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Netflix, Inc. Adjusted Final Closing Prices \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[112]:


NFLX_Data_pct_single= pd.read_pickle('NFLX_data_singlep.pickle')
NFLX_Final_Correlation = NFLX_Data_pct_single.corr()
print(NFLX_Final_Correlation['NFLX Final'].describe())


# In[113]:


NFLX_Data_pct_single= pd.read_pickle('NFLX_data_singlep.pickle')
NFLX_Data_pct_single['NFLX Final Mean'] = NFLX_Data_pct_single['NFLX Final'].rolling(window=12).mean()
NFLX_Data_pct_single['NFLX Final STD'] = NFLX_Data_pct_single['NFLX Final'].rolling(window=12).std() 


# In[114]:


print(NFLX_Data_pct_single[['NFLX Final','NFLX Final Mean']])


# In[115]:


fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

NFLX_Data_pct_single['NFLX Final'].plot(ax=ax1)
NFLX_Data_pct_single['NFLX Final Mean'].plot(ax=ax1)
NFLX_Data_pct_single['NFLX Final STD'].plot(ax=ax2)

plt.title('NFLX Final Adjusted 10 month Rolling Standard Deviation and Mean')

plt.show()


# In[116]:


ntflmutualfunds = pd.read_html('https://money.cnn.com/quote/shareholders/shareholders.html?symb=NFLX&subView=institutional')
print(ntflmutualfunds) # getting mutual fund percentage data from website


# In[117]:


print(ntflmutualfunds[2])# findinga specific dataframe and bring it to light 


# ## Sony Corporation General Data

# In[118]:


style.use('fivethirtyeight')


# In[119]:


df_Sony = web.DataReader("SNE", "yahoo", start, end )
df_Sony.rename(columns={'Adj Close':'SNE Final'}, inplace=True)


# In[120]:


def grab_initial_sne_data():
    
    main_df = pd.DataFrame()
    
    df_Sony = web.DataReader("SNE", "yahoo", start, end )
    df_Sony.rename(columns={'Adj Close':'SNE Final'}, inplace=True)
    
    if main_df.empty:
        main_df = df_Sony
    else:
        main_df = main_df.join(df_Sony)
    
    pickle_out = open('SNE_data.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_sne_data()


# In[121]:


SNE_Data = pd.read_pickle('SNE_data.pickle')
print(SNE_Data)


# In[122]:


SNE_Data[['High','Low','Open','Close','SNE Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Sony Corporation\n15 Year Market Value')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[123]:


SNE_Data[['Volume']].plot()
plt.xlabel('Year')
plt.ylabel('Num of Shares')
plt.title('Sony Corporation \n10 Year Volume')
plt.legend().remove()
plt.subplots_adjust(left=0.12, bottom=0.20, right=0.93, top=0.90, wspace=0.2, hspace=0) # adjust graph size
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[124]:


def grab_initial_sne_data():
    
    main_df = pd.DataFrame()
    
    df_Sony = web.DataReader("SNE", "yahoo", start, end )
    df_Sony.rename(columns={'Adj Close':'SNE Final'}, inplace=True)
    SNE_pct_change = df_Sony.pct_change()
    SNE_pct_change.dropna(how='all',inplace=True) 
    
    if main_df.empty:
        main_df = SNE_pct_change
    else:
        main_df = main_df.join(SNE_pct_change)
    
    pickle_out = open('SNE_data_ptp.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_sne_data()


# In[125]:


SNE_Data_pct= pd.read_pickle('SNE_data_ptp.pickle')
print(SNE_Data_pct.head())


# In[126]:


SNE_Data_pct[['High','Low','Open','Close','SNE Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Sony Corporation \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[127]:


SNE_Data_pct= pd.read_pickle('SNE_data_ptp.pickle')
SNE_Data_Correlation = SNE_Data_pct.corr()
print(SNE_Data_Correlation.describe())


# In[128]:



resample_SNE = SNE_Data_pct.resample('M').mean() # how = 'mean'
print(resample_SNE.head())


# In[129]:


plt.style.use('ggplot')
resample_SNE[['High','Low','Open','Close','SNE Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Sony Corporation \nResampled Percent Change By Month')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[130]:


def grab_initial_sne_data():
    
    
    main_df = pd.DataFrame()
    
    df_Sony = web.DataReader("SNE", "yahoo", start, end )
    df_Sony.rename(columns={'Adj Close':'SNE Final'}, inplace=True)
    
    df_Sony['SNE Final'] = (df_Sony['SNE Final']-df_Sony['SNE Final'][0]) / df_Sony['SNE Final'][0] * 100.0

    df_Sony.dropna(how='all',inplace=True) 


    if main_df.empty:
        main_df = df_Sony
    else:
        main_df = main_df.join(df_Sony)
    
    pickle_out = open('SNE_data_singlep.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_sne_data()


# In[131]:


SNE_Data_pct_single= pd.read_pickle('SNE_data_singlep.pickle')
print(SNE_Data_pct_single.head())


# In[132]:


plt.style.use('classic')
SNE_Data_pct_single= pd.read_pickle('SNE_data_singlep.pickle')
SNE_Data_pct_single[['SNE Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Sony Corporation Adjusted Final Closing Prices \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[133]:


SNE_Data_pct_single= pd.read_pickle('SNE_data_singlep.pickle')
SNE_Final_Correlation = SNE_Data_pct_single.corr()
print(SNE_Final_Correlation['SNE Final'].describe())


# In[134]:


SNE_Data_pct_single= pd.read_pickle('SNE_data_singlep.pickle')
SNE_Data_pct_single['SNE Final Mean'] = SNE_Data_pct_single['SNE Final'].rolling(window=12).mean()
SNE_Data_pct_single['SNE Final STD'] = SNE_Data_pct_single['SNE Final'].rolling(window=12).std() 


# In[135]:


print(SNE_Data_pct_single[['SNE Final','SNE Final Mean']])


# In[136]:


fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

SNE_Data_pct_single['SNE Final'].plot(ax=ax1)
SNE_Data_pct_single['SNE Final Mean'].plot(ax=ax1)
SNE_Data_pct_single['SNE Final STD'].plot(ax=ax2)

plt.title('SNE Final Adjusted 10 month Rolling Standard Deviation and Mean')

plt.show()


# In[137]:


snemutualfunds = pd.read_html('https://money.cnn.com/quote/shareholders/shareholders.html?symb=SNE&subView=institutional')
print(snemutualfunds) # getting mutual fund percentage data from website


# In[138]:


print(snemutualfunds[2])# finding a specific dataframe and bring it to light


# ## Gather all Entertainment Stock

# In[139]:


Disney_df = pd.read_pickle('DIS_data.pickle')
Netflix_df = pd.read_pickle('NFLX_data.pickle')
Sony_df = pd.read_pickle('SNE_data.pickle')


All_Raw_StockE = pd.DataFrame()
All_Raw_Stock_Entertain = All_Raw_StockE.append([Disney_df,Netflix_df,Sony_df])
All_Raw_Stock_Entertain = All_Raw_Stock_Entertain.drop(["High","Low","Open","Close"], axis=1)


# In[140]:


print(All_Raw_Stock_Entertain)


# In[141]:


All_Raw_Stock_Entertain.to_pickle('All_Raw_Stock_Entertain.pickle')


# In[142]:


All_Raw_Stock_Entertain = pd.read_pickle('All_Raw_Stock_Entertain.pickle')
All_Raw_Entertain_p2p = All_Raw_Stock_Entertain.pct_change()


# In[143]:


print(All_Raw_Entertain_p2p.head())


# In[144]:


All_Raw_Entertain_p2p.dropna(inplace=True)
print(All_Raw_Entertain_p2p.head())


# In[145]:


plt.style.use('default')
All_Raw_Entertain_p2p[['DIS Final','NFLX Final','SNE Final']].plot()


plt.legend()
plt.show()


# In[146]:


plt.style.use('grayscale')
All_Raw_Entertain_p2p[['Volume']].plot()
plt.legend()
plt.ylabel('# of Shares by Millions')
plt.show()


# In[147]:


All_Raw_Entertain_p2p.to_pickle('All_Raw_Entertain_p2p.pickle')


# ## All Stocks Analysis

# In[148]:


entertainment_all = pd.read_pickle('All_Raw_Stock_Entertain.pickle') # applying the previous concept except for all of the stocks 
pharma_all = pd.read_pickle('All_Raw_Stock_Pharm.pickle')
All_ofThemPlaceHolder = pd.DataFrame()


# In[149]:


All_The_Stocks_together = All_ofThemPlaceHolder.append([entertainment_all,pharma_all])


# In[150]:


print(All_The_Stocks_together)


# In[151]:


plt.style.use('ggplot')
All_The_Stocks_together[['DIS Final','NFLX Final','SNE Final','PFE Final','JNJ Final','MRK Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Final Adjusted Closing Analysis\nOf All Six Stocks')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[152]:


slices = [All_The_Stocks_together['DIS Final'].mean(),
          All_The_Stocks_together['NFLX Final'].mean(),
          All_The_Stocks_together['SNE Final'].mean(),
          All_The_Stocks_together['PFE Final'].mean(),
          All_The_Stocks_together['JNJ Final'].mean(),
          All_The_Stocks_together['MRK Final'].mean()] 
# using the averages of all of the adjusted closing prices to determine a reliable outcome 

activities = ['Disney','Netflix','Sony','Pfizer','Johnson & Johnson','Merck'] # labelling the pie chart
cols = ['c','m','r','b','y','g'] # determining the colors 
plt.pie(slices,
        labels=activities,
        colors=cols,
        startangle=90,
        shadow=True, # creating a shadow
        explode=(0,0.1,0,0,0,0), # graphic designs 
        autopct='%1.1f%%')
plt.title('Average Percentage of Adjusted Closing Stock Price')
plt.show()


# # Best 3 Stock Portfolio 

# ## Netflix, Inc 
# 
# ![unnamed.jpg](attachment:unnamed.jpg)

# In[153]:


style.use('fivethirtyeight')


# In[154]:


df_Netflix = web.DataReader("NFLX", "yahoo", start, end )
df_Netflix.rename(columns={'Adj Close':'NFLX Final'}, inplace=True)


# In[155]:


def grab_initial_nflx_data():
    
    main_df = pd.DataFrame()
    
    df_Netflix = web.DataReader("NFLX", "yahoo", start, end )
    df_Netflix.rename(columns={'Adj Close':'NFLX Final'}, inplace=True)
    
    if main_df.empty:
        main_df = df_Netflix
    else:
        main_df = main_df.join(df_Netflix)
    
    pickle_out = open('NFLX_data.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_nflx_data()


# In[156]:


NFLX_Data = pd.read_pickle('NFLX_data.pickle')
print(NFLX_Data)


# In[157]:


NFLX_Data[['High','Low','Open','Close','NFLX Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Netflix, Inc.\n15 Year Market Value')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[158]:


NFLX_Data[['Volume']].plot()
plt.xlabel('Year')
plt.ylabel('Num of Shares')
plt.title('Netflix, Inc. \n10 Year Volume')
plt.legend().remove()
plt.subplots_adjust(left=0.12, bottom=0.20, right=0.93, top=0.90, wspace=0.2, hspace=0) # adjust graph size
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[159]:


def grab_initial_nflx_data():
    
    main_df = pd.DataFrame()
    
    df_Netflix = web.DataReader("NFLX", "yahoo", start, end )
    df_Netflix.rename(columns={'Adj Close':'NFLX Final'}, inplace=True)
    NFLX_pct_change = df_Netflix.pct_change()
    NFLX_pct_change.dropna(how='all',inplace=True) 
    
    if main_df.empty:
        main_df = NFLX_pct_change
    else:
        main_df = main_df.join(NFLX_pct_change)
    
    pickle_out = open('NFLX_data_ptp.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_nflx_data()


# In[160]:


NFLX_Data_pct= pd.read_pickle('NFLX_data_ptp.pickle')
print(NFLX_Data_pct.head())


# In[161]:


NFLX_Data_pct[['High','Low','Open','Close','NFLX Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Netflix, Inc. \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[162]:


NFLX_Data_pct= pd.read_pickle('NFLX_data_ptp.pickle')
NFLX_Data_Correlation = NFLX_Data_pct.corr()
print(NFLX_Data_Correlation.describe())


# In[163]:


resample_NFLX = NFLX_Data_pct.resample('M').mean() # how = 'mean'
print(resample_NFLX.head())


# In[164]:


plt.style.use('ggplot')
resample_NFLX[['High','Low','Open','Close','NFLX Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Netflix, Inc. \nResampled Percent Change By Month')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[165]:


def grab_initial_nflx_data():
    
    
    main_df = pd.DataFrame()
    
    df_Netflix = web.DataReader("NFLX", "yahoo", start, end )
    df_Netflix.rename(columns={'Adj Close':'NFLX Final'}, inplace=True)
    
    df_Netflix['NFLX Final'] = (df_Netflix['NFLX Final']-df_Netflix['NFLX Final'][0]) / df_Netflix['NFLX Final'][0] * 100.0

    df_Netflix.dropna(how='all',inplace=True) 


    if main_df.empty:
        main_df = df_Netflix
    else:
        main_df = main_df.join(df_Netflix)
    
    pickle_out = open('NFLX_data_singlep.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_nflx_data()


# In[166]:


NFLX_Data_pct_single= pd.read_pickle('NFLX_data_singlep.pickle')
print(NFLX_Data_pct_single.head())


# In[167]:


plt.style.use('classic')
NFLX_Data_pct_single= pd.read_pickle('NFLX_data_singlep.pickle')
NFLX_Data_pct_single[['NFLX Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Netflix, Inc. Adjusted Final Closing Prices \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[168]:


NFLX_Data_pct_single= pd.read_pickle('NFLX_data_singlep.pickle')
NFLX_Final_Correlation = NFLX_Data_pct_single.corr()
print(NFLX_Final_Correlation['NFLX Final'].describe())


# In[169]:


NFLX_Data_pct_single= pd.read_pickle('NFLX_data_singlep.pickle')
NFLX_Data_pct_single['NFLX Final Mean'] = NFLX_Data_pct_single['NFLX Final'].rolling(window=12).mean()
NFLX_Data_pct_single['NFLX Final STD'] = NFLX_Data_pct_single['NFLX Final'].rolling(window=12).std() 


# In[170]:


print(NFLX_Data_pct_single[['NFLX Final','NFLX Final Mean']])


# In[171]:


fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

NFLX_Data_pct_single['NFLX Final'].plot(ax=ax1)
NFLX_Data_pct_single['NFLX Final Mean'].plot(ax=ax1)
NFLX_Data_pct_single['NFLX Final STD'].plot(ax=ax2)

plt.title('NFLX Final Adjusted 10 month Rolling Standard Deviation and Mean')

plt.show()


# ## The Walt Disney Company 
# ![waltdisneylogo.jpg](attachment:waltdisneylogo.jpg)

# In[172]:


style.use('fivethirtyeight')


# In[173]:


df_Disney = web.DataReader("DIS", "yahoo", start, end )
df_Disney.rename(columns={'Adj Close':'DIS Final'}, inplace=True)


# In[174]:


def grab_initial_dis_data():
    
    main_df = pd.DataFrame()
    
    df_Disney = web.DataReader("DIS", "yahoo", start, end )
    df_Disney.rename(columns={'Adj Close':'DIS Final'}, inplace=True)
    
    if main_df.empty:
        main_df = df_Disney
    else:
        main_df = main_df.join(df_Disney)
    
    pickle_out = open('DIS_data.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_dis_data()


# In[175]:


DIS_Data = pd.read_pickle('DIS_data.pickle')
print(DIS_Data)


# pickle_in = open('DIS_data.pickle','rb')
# DIS_Data = pickle.load(pickle_in)
# pickle_in.close()


# In[176]:


DIS_Data[['High','Low','Open','Close','DIS Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('The Walt Disney Company  \n15 Year Market Value')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[177]:


DIS_Data[['Volume']].plot()
plt.xlabel('Year')
plt.ylabel('Num of Shares')
plt.title('The Walt Disney Company \n15 Year Volume')
plt.legend().remove()
plt.subplots_adjust(left=0.12, bottom=0.20, right=0.93, top=0.90, wspace=0.2, hspace=0) # adjust graph size
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[178]:


def grab_initial_dis_data():
    
    main_df = pd.DataFrame()
    
    df_Disney = web.DataReader("DIS", "yahoo", start, end )
    df_Disney.rename(columns={'Adj Close':'DIS Final'}, inplace=True)
    DIS_pct_change = df_Disney.pct_change()
    DIS_pct_change.dropna(how='all',inplace=True) 
    
    if main_df.empty:
        main_df = DIS_pct_change
    else:
        main_df = main_df.join(DIS_pct_change)
    
    pickle_out = open('DIS_data_ptp.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_dis_data()


# In[179]:


DIS_Data_pct= pd.read_pickle('DIS_data_ptp.pickle')
print(DIS_Data_pct.head())


# In[180]:


DIS_Data_pct[['High','Low','Open','Close','DIS Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('The Walt Disney Company \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[181]:


DIS_Data_pct= pd.read_pickle('DIS_data_ptp.pickle')
DIS_Data_Correlation = DIS_Data_pct.corr()
print(DIS_Data_Correlation.describe())


# In[182]:


resample_DIS = DIS_Data_pct.resample('M').mean() # how = 'mean'
print(resample_DIS.head())


# In[183]:


plt.style.use('ggplot')
resample_DIS[['High','Low','Open','Close','DIS Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('The Walt Disney Company \nResampled Percent Change By Month')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[184]:


def grab_initial_dis_data():
    
    
    main_df = pd.DataFrame()
    
    df_Disney = web.DataReader("DIS", "yahoo", start, end )
    df_Disney.rename(columns={'Adj Close':'DIS Final'}, inplace=True)
    
    df_Disney['DIS Final'] = (df_Disney['DIS Final']-df_Disney['DIS Final'][0]) / df_Disney['DIS Final'][0] * 100.0

    df_Disney.dropna(how='all',inplace=True) 


    if main_df.empty:
        main_df = df_Disney
    else:
        main_df = main_df.join(df_Disney)
    
    pickle_out = open('DIS_data_singlep.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_dis_data()


# In[185]:


DIS_Data_pct_single= pd.read_pickle('DIS_data_singlep.pickle')
print(DIS_Data_pct_single.head())


# In[186]:


plt.style.use('classic')
DIS_Data_pct_single= pd.read_pickle('DIS_data_singlep.pickle')
DIS_Data_pct_single[['DIS Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('The Walt Disney Company Adjusted Final Closing Prices \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[187]:


DIS_Data_pct_single= pd.read_pickle('DIS_data_singlep.pickle')
DIS_Final_Correlation = DIS_Data_pct_single.corr()
print(DIS_Final_Correlation['DIS Final'].describe())


# In[188]:


DIS_Data_pct_single= pd.read_pickle('DIS_data_singlep.pickle')
DIS_Data_pct_single['DIS Final Mean'] = DIS_Data_pct_single['DIS Final'].rolling(window=12).mean()
DIS_Data_pct_single['DIS Final STD'] = DIS_Data_pct_single['DIS Final'].rolling(window=12).std() 


# In[189]:


print(DIS_Data_pct_single[['DIS Final','DIS Final Mean']])


# In[190]:


fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

DIS_Data_pct_single['DIS Final'].plot(ax=ax1)
DIS_Data_pct_single['DIS Final Mean'].plot(ax=ax1)
DIS_Data_pct_single['DIS Final STD'].plot(ax=ax2)

plt.title('DIS Final Adjusted 10 month Rolling Standard Deviation and Mean')

plt.show()


# ## Johnson & Johnson 
# ![downloadsdf.jfif](attachment:downloadsdf.jfif)

# In[191]:



df_Johnson = web.DataReader("JNJ", "yahoo", start, end )
df_Johnson.rename(columns={'Adj Close':'JNJ Final'}, inplace=True)


# In[192]:




def grab_initial_jnj_data():
    
    main_df = pd.DataFrame()
    
    df_Johnson = web.DataReader("JNJ", "yahoo", start, end )
    df_Johnson.rename(columns={'Adj Close':'JNJ Final'}, inplace=True)
    
    if main_df.empty:
        main_df = df_Johnson
    else:
        main_df = main_df.join(df_Johnson)
    
    pickle_out = open('JNJ_data.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_jnj_data()


# In[193]:



JNJ_Data = pd.read_pickle('JNJ_data.pickle')
print(JNJ_Data)


# In[194]:


JNJ_Data[['High','Low','Open','Close','JNJ Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Johnson & Johnson \n10 Year Market Value')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[195]:


JNJ_Data[['Volume']].plot()
plt.xlabel('Year')
plt.ylabel('Num of Shares')
plt.title('Johnson & Johnson Inc. \n15 Year Volume')
plt.legend().remove()
plt.subplots_adjust(left=0.12, bottom=0.20, right=0.93, top=0.90, wspace=0.2, hspace=0) # adjust graph size
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[196]:


def grab_initial_jnj_data():
    
    main_df = pd.DataFrame()
    
    df_Johnson = web.DataReader("JNJ", "yahoo", start, end )
    df_Johnson.rename(columns={'Adj Close':'JNJ Final'}, inplace=True)
    JNJ_pct_change = df_Johnson.pct_change()
    JNJ_pct_change.dropna(how='all',inplace=True) 
    
    if main_df.empty:
        main_df = JNJ_pct_change
    else:
        main_df = main_df.join(JNJ_pct_change)
    
    pickle_out = open('JNJ_data_ptp.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_jnj_data()


# In[197]:


JNJ_Data_pct= pd.read_pickle('JNJ_data_ptp.pickle')
print(JNJ_Data_pct.head())


# In[198]:



JNJ_Data_pct[['High','Low','Open','Close','JNJ Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Johnson & Johnson\n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 0.5
plt.show()


# In[199]:


JNJ_Data_pct= pd.read_pickle('JNJ_data_ptp.pickle')
JNJ_Data_Correlation = JNJ_Data_pct.corr()
print(JNJ_Data_Correlation.describe())


# In[200]:


resample_JNJ = JNJ_Data_pct.resample('M').mean() # how = 'mean'
print(resample_JNJ.head())


# In[201]:


plt.style.use('ggplot')
resample_JNJ[['High','Low','Open','Close','JNJ Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Johnson & Johnson\nResampled Percent Change By Month')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[202]:



def grab_initial_jnj_data():
    
    
    main_df = pd.DataFrame()
    
    df_Johnson = web.DataReader("JNJ", "yahoo", start, end )
    df_Johnson.rename(columns={'Adj Close':'JNJ Final'}, inplace=True)
    
    df_Johnson['JNJ Final'] = (df_Johnson['JNJ Final']-df_Johnson['JNJ Final'][0]) / df_Johnson['JNJ Final'][0] * 100.0

    df_Johnson.dropna(how='all',inplace=True) 


    if main_df.empty:
        main_df = df_Johnson
    else:
        main_df = main_df.join(df_Johnson)
    
    pickle_out = open('JNJ_data_singlep.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
grab_initial_jnj_data()


# In[203]:


JNJ_Data_pct_single= pd.read_pickle('JNJ_data_singlep.pickle')
print(JNJ_Data_pct_single.head())


# In[204]:


plt.style.use('classic')
JNJ_Data_pct_single= pd.read_pickle('JNJ_data_singlep.pickle')
JNJ_Data_pct_single[['JNJ Final']].plot()
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.title('Johnson& Johnson Adjusted Final Closing Prices \n15 Year Percent Change')
plt.legend(markerfirst=False)
plt.rcParams['lines.linewidth'] = 2.0
plt.show()


# In[205]:


JNJ_Data_pct_single= pd.read_pickle('JNJ_data_singlep.pickle')
JNJ_Final_Correlation = JNJ_Data_pct_single.corr()
print(JNJ_Final_Correlation['JNJ Final'].describe())


# In[206]:


JNJ_Data_pct_single= pd.read_pickle('JNJ_data_singlep.pickle')
JNJ_Data_pct_single['JNJ Final Mean'] = JNJ_Data_pct_single['JNJ Final'].rolling(window=12).mean()
JNJ_Data_pct_single['JNJ Final STD'] = JNJ_Data_pct_single['JNJ Final'].rolling(window=12).std() 


# In[207]:


print(JNJ_Data_pct_single[['JNJ Final','JNJ Final Mean']])


# In[208]:


fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

JNJ_Data_pct_single['JNJ Final'].plot(ax=ax1)
JNJ_Data_pct_single['JNJ Final Mean'].plot(ax=ax1)
JNJ_Data_pct_single['JNJ Final STD'].plot(ax=ax2)

plt.title('JNJ Final Adjusted 10 month Rolling Standard Deviation and Mean')

plt.show()


# ## Best Three Comparison

# In[209]:


Disney_df = pd.read_pickle('DIS_data.pickle')
Netflix_df = pd.read_pickle('NFLX_data.pickle')
Johnson_df = pd.read_pickle('JNJ_data.pickle')


All_Best = pd.DataFrame()
All_Best_Stock = All_Best.append([Disney_df,Netflix_df,Johnson_df])
All_Best_Stock = All_Best_Stock.drop(["High","Low","Open","Close"], axis=1)


# In[210]:


print(All_Best_Stock)


# In[211]:


All_Best_Stock.to_pickle('All_Best_Stock.pickle')


# In[212]:


All_Best_Stock = pd.read_pickle('All_Best_Stock.pickle')
All_Best_Stock_p2p = All_Best_Stock.pct_change()


# In[213]:


print(All_Best_Stock_p2p.head())


# In[214]:


All_Best_Stock_p2p.dropna(inplace=True)
print(All_Best_Stock_p2p.head())


# In[215]:


plt.style.use('ggplot')
All_Best_Stock[['DIS Final','NFLX Final','JNJ Final']].plot()
              
plt.legend()
plt.show()


# In[216]:


plt.style.use('grayscale')
All_Best_Stock_p2p[['Volume']].plot()
plt.legend()
plt.ylabel('# of Shares by Millions')
plt.show()


# In[217]:


All_Best_Stock_p2p.to_pickle('All_Best_Stock_p2p.pickle')


# # Conclusion of the Three Portfolios 

# It seems as though most profitable and best stocks to invest come from the entertainment industry. 2/3 of the best portfolio is a part of the entertainment industry, the stocks being 
# 1. **Netflix** 
# 2. **Disney** 
# 3. and the last one being **Johnson & Johnson**.
# ----
# 

# In[ ]:




