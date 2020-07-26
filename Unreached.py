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


# In[4]:


import io
import requests


# # Import Unreached Base File

# In[5]:


url = "https://joshuaproject.net/resources/datasets/1"
response = requests.get(url)


# In[6]:


open('unreached.csv','wb').write(response.content)


# In[7]:


ur_df = pd.read_csv('unreached.csv', low_memory=False,skiprows=1)


# All Columns: ROG, Ctry, PeopleID3, ROP3, PeopNameAcrossCountries, PeopNameInCountry, Population, JPScale, LeastReached, ROL3, PrimaryLanguageName, BibleStatus, RLG3, PrimaryReligion, PercentAdherents, PercentEvangelical, PeopleID1, ROP1, AffinityBloc, PeopleID2, ROP2, PeopleCluster, CountOfCountries, RegionCode, RegionName, ROG2, Continent, 10_40Window, IndigenousCode, WorkersNeeded, Frontier, Latitude, Longitude

# In[8]:


ur_df.head()


# In[9]:


ur_df.describe()


# ## Analyze Data

# In[10]:


ur_df['quartile'] = pd.qcut(ur_df['PercentEvangelical'], q=4, duplicates='drop')
ur_df['decile'] = pd.qcut(ur_df['PercentEvangelical'], q=10, precision=3, duplicates='drop')


# In[11]:


ur_df.head()


# # Map Visualization

# In[12]:


ur_df_plot = ur_df


# In[13]:


ur_df_plot = ur_df_plot[~pd.isna(ur_df['Population'])]


# In[14]:


ur_df_plot = ur_df_plot[~pd.isna(ur_df['decile'])]


# In[15]:


ur_df_plot = ur_df_plot[ur_df_plot['LeastReached'] == 'Y']


# In[16]:


lat = ur_df_plot['Latitude'].values
lon = ur_df_plot['Longitude'].values


# In[50]:


ur_df_plot.head()


# ## Matplotlib (Static)

# In[17]:


# # Following based on https://jakevdp.github.io/PythonDataScienceHandbook/04.13-geographic-data-with-basemap.html
# #Matplotlib maps appear to be static, investigating interactive maps
# # 1. Draw the map background
# fig = plt.figure(figsize=(12, 8), edgecolor='w')
# m = Basemap(projection='cyl', resolution=None,
#             llcrnrlat=-90, urcrnrlat=90,
#             llcrnrlon=-180, urcrnrlon=180)
# m.shadedrelief()
# # 2. scatter city data, with color reflecting population
# # and size reflecting area
# m.scatter(lon, lat, latlon=True, alpha=0.1)

# #  To be adapted:

# # # 3. create colorbar and legend
# # plt.colorbar(label=r'$\log_{10}({\rm population})$')
# # plt.clim(3, 7)

# # # make legend with dummy points
# # for a in [100, 300, 500]:
# #     plt.scatter([], [], c='k', alpha=0.5, s=a,
# #                 label=str(a) + ' km$^2$')
# # plt.legend(scatterpoints=1, frameon=False,
# #            labelspacing=1, loc='lower left');


# ## Plotly (Interactive)

# In[ ]:


#From https://plotly.com/python/scatter-plots-on-maps/

px.set_mapbox_access_token("pk.eyJ1IjoicGFzYXVsIiwiYSI6ImNrZDB1MHJqZzB4Yjkycm15MHZkZmRpa3gifQ.mciD4JDnZFXAhyOgm_8oww")
fig = px.scatter_mapbox(ur_df_plot, lat="Latitude",
                     lon = "Longitude",
                     color="PercentEvangelical", # which column to use to set the color of markers
                     hover_name="PeopNameInCountry", # column added to hover information
                     size="Population", # size of markers
                     color_continuous_scale=px.colors.cyclical.IceFire_r,
                     size_max=15,
                     zoom=10)
# fig.update_layout(mapbox_style="open-street-map")
fig.show()


# In[43]:


#From https://plotly.com/python/scatter-plots-on-maps/

df = px.data.carshare()
df.head()
fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon",     color="peak_hour", size="car_hours",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
fig.show()


# In[49]:


df.head()


# In[32]:


colors = ['Red','OrangeRed','Orange','Yellow']
px.set_mapbox_access_token('pk.eyJ1IjoicGFzYXVsIiwiYSI6ImNrZDB1MHJqZzB4Yjkycm15MHZkZmRpa3gifQ.mciD4JDnZFXAhyOgm_8oww')
fig = px.scatter_geo(ur_df_plot, lat='Latitude',
                     lon = 'Longitude',
                     color="PercentEvangelical", # which column to use to set the color of markers
                     hover_name="PeopNameInCountry", # column added to hover information
                     size="Population", # size of markers
                     color_continuous_scale=px.colors.cyclical.IceFire_r)

fig.show()

