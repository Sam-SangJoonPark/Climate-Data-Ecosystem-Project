#!/usr/bin/env python
# coding: utf-8

# # Data Source 1 - Geography Reference

# ## MSA_GEOGRAPHY_REF file (2022 version)

# ## Raw data source:
# 
# https://www.census.gov/programs-surveys/cbp/technical-documentation/reference/metro-area-geography-reference.html

# In[12]:


import sys
sys.path.append('../../scripts')  
import merging_utils
import yaml
import pandas as pd

with open("../../config/preprocessing.yaml", "r") as f:
    preprocessing_config = yaml.safe_load(f)

version = 2022
prefix = preprocessing_config['geo_ref'][version]['prefix']


# In[13]:


url = "https://www2.census.gov/programs-surveys/cbp/technical-documentation/reference/metro-area-geography-reference/msa_county_reference22.txt"

# Load the data
df = pd.read_csv(url, encoding='cp1252', quotechar='"')


# In[14]:


df.head(5)


# In[15]:


df.info()


# In[16]:


df.describe()


# In[17]:


df.to_csv('../../data/raw/msa_county_reference22.csv',index=False)


# In[18]:


print('Before adding prefixes: ' , df.columns)
df = merging_utils.add_prefix_all(df, prefix=prefix)
print('After adding prefixes: ' , df.columns)


# In[19]:


df


# In[21]:


df.to_csv('../../data/interim/data1.csv',index=False)

