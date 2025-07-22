#!/usr/bin/env python
# coding: utf-8

# # Data Source 4 - Migration

# ### Raw Data Source

# https://www.census.gov/data/tables/2020/demo/geographic-mobility/metro-to-metro-migration.html
# 

# ### Explanation about data

# PDF: https://www.census.gov/programs-surveys/acs/technical-documentation/code-lists.html
# 
# - Code Lists, Definitions, and Accuracy

# In[1]:


import sys
sys.path.append('../../scripts')  
import merging_utils
import yaml
import pandas as pd
import numpy as np

with open("../../config/preprocessing.yaml", "r") as f:
    preprocessing_config = yaml.safe_load(f)

prefix = preprocessing_config['migration']['prefix']
exclude_region = preprocessing_config['migration']['exclude_region']


# In[2]:


file_name = '../../data/raw/metro-to-metro-ins-outs-nets-gross-2016-2020.xlsx'


# ## Set the header

# In[3]:


df = pd.read_excel(file_name)


# In[4]:


# multi-row column headers
df.head(5)


# In[5]:


df.columns[0]


# ## Multi level Column

# In[6]:


# multi-level column index (row 1 and 2)
df = pd.read_excel(file_name, header=[1, 2])


# In[7]:


df.head(3)


# In[8]:


df.columns = [
    '_'.join([str(i).strip() for i in col if str(i).strip().lower() != 'nan' and not str(i).startswith('Unnamed')])
    for col in df.columns
]


# In[9]:


df.head(3)


# ## Delete the footnote

# In[10]:


df.tail(10)


# In[11]:


df = df.iloc[:-7]


# In[12]:


# no footnote included
df


# ## Removing Footnote markers

# ![image.png](attachment:39c202a9-db41-43ea-ab03-51282461db3f.png)

# In[13]:


df.head(3)


# In[14]:


import re
print(df.columns)
df.columns = [re.sub(r'(Geography [AB])\d+', r'\1', col) for col in df.columns]
print(df.columns)


# ## Group by - MSA Level

# ## ACS data aggregation method (PDF from the Bureau of Census)

# ![image.png](attachment:9b79e29b-3c3b-4824-81a4-9e835301b4ae.png)

# ### Exclude unnecessary columns

# In[15]:


df_filtered = df[
    (~df['Metro Code of Geography A'].isin(exclude_region)) &
    (~df['Metro Code of Geography B'].isin(exclude_region))
]


# In[16]:


# List of estimate and MOE column name pairs
estimate_moe_pairs = [
    ('Flow from Geography B to Geography A_Estimate', 'Flow from Geography B to Geography A_MOE'),
    ('Counterflow from Geography A to Geography B_Estimate', 'Counterflow from Geography A to Geography B_MOE'),
    ('Net Migration from Geography B to Geography A_Estimate', 'Net Migration from Geography B to Geography A_MOE'),
    ('Gross Migration between Geography A and Geography B_Estimate', 'Gross Migration between Geography A and Geography B_MOE')
]


# Function to sum estimates and calculate combined MOEs
# calculation method in PDF "Instructions for Applying Statistical Testing to American Community Survey Data" page 3
def aggregate_msa_level(df, group_col='Metro Code of Geography A'):
    grouped = df.groupby(group_col)
    result = grouped.agg(
        {est: 'sum' for est, _ in estimate_moe_pairs} |
        {moe: lambda x: np.sqrt((x**2).sum()) for _, moe in estimate_moe_pairs}
    ).reset_index()
    return result

# Apply the function
msa_level_df = aggregate_msa_level(df_filtered)


# In[17]:


# Column B =  Column C + Column D
msa_level_df


# ## Column readability

# ### Rename columns to reflect their meanings

# In[18]:


msa_level_df = msa_level_df.rename(columns={
    'Flow from Geography B to Geography A_Estimate': 'A_Inflow_Estimate',
    'Flow from Geography B to Geography A_MOE': 'A_Inflow_MOE',
    'Counterflow from Geography A to Geography B_Estimate': 'A_Outflow_Estimate',
    'Counterflow from Geography A to Geography B_MOE': 'A_Outflow_MOE',
    'Net Migration from Geography B to Geography A_Estimate': 'A_NetMigration_Estimate',
    'Net Migration from Geography B to Geography A_MOE': 'A_NetMigration_MOE',
    'Gross Migration between Geography A and Geography B_Estimate': 'A_GrossMigration_Estimate',
    'Gross Migration between Geography A and Geography B_MOE': 'A_GrossMigration_MOE'
})


# ## Adding Prefixes in columns

# In[19]:


print('Before adding prefixes: ' , msa_level_df.columns)
msa_level_df = merging_utils.add_prefix_all(msa_level_df, prefix=prefix)
print()
print('After adding prefixes: ' , msa_level_df.columns)


# In[20]:


msa_level_df.to_csv('../../data/interim/data4_migration.csv',index=False)

