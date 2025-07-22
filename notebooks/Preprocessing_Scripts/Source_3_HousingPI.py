#!/usr/bin/env python
# coding: utf-8

# # Data Source 3 - Housing

# # Version 1 - 2025 update

# ### Raw data Source

# https://docs.google.com/spreadsheets/d/1L5nTOVlTZ-WSxgXwvV5rmIKNL7Rm7msQxbYqZ2YHsLs/edit?gid=0#gid=0
# 

# ### Explanation about data

# https://www.jchs.harvard.edu/son-2025-price-to-income-map

# # Version 2 - 2022 update

# ### Raw Data Source

# https://docs.google.com/spreadsheets/d/1inBM5dtDSOvLrkfOSRC07eeIsOY8TkDrhtuu5Zp8t3Y/edit?gid=547532302#gid=547532302

# ### Explanation about data

# https://www.jchs.harvard.edu/blog/home-price-income-ratio-reaches-record-high-0

# ## Select the year

# In[1]:


version = 2025


# In[4]:


import sys
sys.path.append('../../scripts')  
import merging_utils
import yaml
import pandas as pd

with open("../../config/preprocessing.yaml", "r") as f:
    preprocessing_config = yaml.safe_load(f)

prefix = preprocessing_config['housing'][version]['prefix']


# In[5]:


path = '../../data/raw/'
file_name = preprocessing_config['housing'][version]['file_name']


# In[6]:


df = pd.read_csv(path+file_name)


# In[7]:


df.info()


# In[8]:


# GEOID, GEOID.1 are the same column
df[df['GEOID'] != df['GEOID.1']]


# In[9]:


print('Before adding prefixes: ' , df.columns)
df = merging_utils.add_prefix_all(df, prefix=prefix)
print()
print('After adding prefixes: ' , df.columns)


# In[10]:


df.to_csv(f'../../data/interim/data3_housing_{version}.csv',index=False)

