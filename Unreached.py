#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os


# In[2]:


os.environ['PROJ_LIB'] = '/Users/patricksaul/anaconda3/share/proj'


# In[3]:


import plotly.express as px
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import datetime as dt


# In[4]:


import io
import requests


# # Import People Groups Base File

# In[5]:


#Data set for all people groups
url = "https://joshuaproject.net/resources/datasets/1"
response = requests.get(url)


# In[6]:


todayFileName = 'AllPeoplesByCountry_' + str(dt.datetime.today().date()) + '.csv'


# In[7]:


open(todayFileName,'wb').write(response.content)


# In[8]:


pg_df = pd.read_csv(todayFileName, low_memory=False,skiprows=1)


# All Columns: ROG, Ctry, PeopleID3, ROP3, PeopNameAcrossCountries, PeopNameInCountry, Population, JPScale, LeastReached, ROL3, PrimaryLanguageName, BibleStatus, RLG3, PrimaryReligion, PercentAdherents, PercentEvangelical, PeopleID1, ROP1, AffinityBloc, PeopleID2, ROP2, PeopleCluster, CountOfCountries, RegionCode, RegionName, ROG2, Continent, 10_40Window, IndigenousCode, WorkersNeeded, Frontier, Latitude, Longitude

# In[9]:


pg_df.head()


# In[10]:


pg_df.describe()


# # Track Changes Over Time (WIP)

# In[20]:


olddt = '2020-06-29'
newdt = str(dt.datetime.today().date())


# In[21]:


old_df = pd.read_csv('AllPeoplesByCountry_' + olddt + '.csv', low_memory=False,skiprows=1)
new_df = pd.read_csv('AllPeoplesByCountry_' + newdt + '.csv', low_memory=False,skiprows=1)


# In[22]:


old_df['Snapshot Date'] = olddt


# In[23]:


new_df['Snapshot Date'] = newdt


# In[24]:


#Concatenate old and new
full_df = pd.concat([old_df,new_df])


# In[25]:


change_df = full_df.drop_duplicates(keep='last')


# In[26]:


full_df = pd.concat([old_df,change_df])


# In[27]:


full_df['ID'] = full_df['PeopleID3'].astype(str).str.cat(full_df['Ctry'], sep=' ')


# In[28]:


full_df = full_df.sort_values(by=['ID'])


# In[29]:


full_df.head()


# In[30]:


# Method below highly inefficient so commented out, but descriptive of the logic we are executing with the NumPy Where
#function below
# ##Iterate through to calculate change
# def changeCalc(df, calcField, outField):
#     prevIdx = None
#     currLoc = 0
#     for index, row in df.iterrows():
#         #If previous row and current row are the same
#         if prevIdx == index:
#             #Subtract the current row's calcField from the previous row's calcField and store in the df at
#             #current integer based position
#             df.iloc[:,(currLoc,outField)] = row[calcField] - df.iloc[:,(currLoc - 1,calcField)]
#         prevIdx = index
#         currLoc +=1

        
# full_df = changeCalc(full_df, 'PercentEvangelical', 'PercEvChg')

full_df['PercEvChg'] = np.where(full_df['ID'].shift(1) == full_df['ID'], full_df['PercentEvangelical'] -                                full_df.shift(1)['PercentEvangelical'],np.NaN)


# In[31]:


full_df[(full_df['PercEvChg'] != 0) & (~pd.isna(full_df['PercEvChg']))]


# # Map Visualization Prep

# In[32]:


ur_df_plot = full_df


# In[33]:


ur_df_plot = ur_df_plot.drop_duplicates(keep='last')


# In[34]:


ur_df_plot = ur_df_plot[~pd.isna(ur_df_plot['Population'])]


# In[35]:


ur_df_plot = ur_df_plot[ur_df_plot['LeastReached'] == 'Y']


# In[36]:


lat = ur_df_plot['Latitude'].values
lon = ur_df_plot['Longitude'].values


# In[37]:


ur_df_plot.head()


# ## Plotly (Interactive)

# In[38]:


#From https://plotly.com/python/scatter-plots-on-maps/
#Size by population, color by # evangelical

px.set_mapbox_access_token(open('mapbox_token.txt').read())
fig1 = px.scatter_mapbox(ur_df_plot, lat="Latitude",
                     lon = "Longitude",
                     color="PercentEvangelical", # which column to use to set the color of markers
                     hover_name="PeopNameInCountry", # column added to hover information
                     size="Population", # size of markers
                     color_continuous_scale=px.colors.sequential.YlOrRd_r,
                     zoom=0.5)
# fig.update_layout(mapbox_style="open-street-map")
fig1.show()


# In[39]:


#From https://plotly.com/python/scatter-plots-on-maps/
#Size by population, color by % change evangelical
#Need to fix visual

chgPlot = ur_df_plot.loc[ur_df_plot['PercEvChg'] != 0]
chgPlot = chgPlot[~pd.isna(chgPlot['PercEvChg'])]

px.set_mapbox_access_token(open('mapbox_token.txt').read())
fig2 = px.scatter_mapbox(chgPlot, lat="Latitude",
                     lon = "Longitude",
                     color="PercEvChg", # which column to use to set the color of markers
                     hover_name="PeopNameInCountry", # column added to hover information
                     size="Population", # size of markers
                     color_continuous_scale=px.colors.sequential.YlOrRd_r,
                     zoom=0.5)
# fig.update_layout(mapbox_style="open-street-map")
fig2.show()


# In[40]:


print(chgPlot['PercEvChg'].min())


# In[41]:


chgPlot[chgPlot['PercEvChg'] == -20]

