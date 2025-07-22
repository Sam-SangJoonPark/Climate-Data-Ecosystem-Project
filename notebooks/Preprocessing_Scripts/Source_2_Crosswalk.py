#!/usr/bin/env python
# coding: utf-8

# # Data Source 2 - Crosswalk

# # Crosswalk - 2023 & 2013 Versions

# ## Raw data source:
# https://www.bls.gov/cew/classifications/areas/county-msa-csa-crosswalk.htm
# 
# - contains both 2013 and 2023 version

# ## Select the year

# In[1]:


version = 2023


# In[2]:


import sys
sys.path.append('../../scripts')  
import merging_utils
import yaml
import pandas as pd

with open("../../config/preprocessing.yaml", "r") as f:
    preprocessing_config = yaml.safe_load(f)

prefix = preprocessing_config['crosswalk'][version]['prefix']
agg_method = preprocessing_config['crosswalk'][version]['agg_method']
file_name = preprocessing_config['crosswalk'][version]['file_name']
path = '../../data/raw/'


# aggregate columns
cbsa_code = preprocessing_config['crosswalk'][version]['cbsa_code']
cbsa_title = preprocessing_config['crosswalk'][version]['cbsa_title']
cbsa_state = preprocessing_config['crosswalk'][version]['cbsa_state']


# In[3]:


prefix, agg_method


# In[4]:


cbsa_code, cbsa_title, cbsa_state


# In[5]:


df = pd.read_excel(path + file_name, header=0)


# ## Set the header

# In[6]:


df.head(5)


# In[7]:


print(df.iloc[0,0])


# In[8]:


df = pd.read_excel(path + file_name, header=2, dtype={'FIPS County Code': str, 'FIPS State Code': str})
df.head(3)


# ## Delete the footnote

# In[9]:


df.tail(3)


# In[10]:


df = df.iloc[:-3]


# In[11]:


df.tail(3)


# In[12]:


df.info()


# In[13]:


df.isnull().sum()


# In[14]:


df.head()


# ## Creating a KEY
# ### FIPS Key is a 5-digit key combining the state and the county code

# In[15]:


df.dtypes


# In[16]:


df['FIPS_Key'] = df['FIPS State Code'] + df['FIPS County Code']


# In[17]:


df


# ## Adding a prefix 

# In[18]:


print('Before adding prefixes: ' , df.columns)

df = merging_utils.add_prefix_all(df, prefix=prefix)

print()
print('After adding prefixes: ' , df.columns)


# In[20]:


df.to_csv(f'../../data/interim/data2_county_level_{version}.csv',index=False)


# ## Group by at the MSA Level

# ## Merge type : Example

# In[21]:


example_common = merging_utils.get_msa_summary(size='metro', df = df, agg_method= 'most_common', prefix=prefix, cbsa_code=cbsa_code, cbsa_title=cbsa_title, cbsa_state=cbsa_state)


# In[22]:


example_common[example_common[cbsa_code] == '17980']


# In[23]:


example_concat =merging_utils.get_msa_summary(size='metro', df = df, agg_method= 'concat', prefix=prefix, cbsa_code=cbsa_code, cbsa_title=cbsa_title, cbsa_state=cbsa_state)


# In[24]:


example_concat[example_concat[cbsa_code] == '17980']


# ## Select the Merge ty[e

# In[25]:


msa_summary =merging_utils.get_msa_summary(size='metro', df = df, agg_method= agg_method, prefix=prefix, cbsa_code=cbsa_code, cbsa_title=cbsa_title, cbsa_state=cbsa_state)


# In[26]:


len(msa_summary)


# In[28]:


msa_summary.to_csv(f'../../data/interim/data2_msa_level_{version}.csv', index=False)

