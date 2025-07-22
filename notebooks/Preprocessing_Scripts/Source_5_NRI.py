#!/usr/bin/env python
# coding: utf-8

# # Data Source 5 - Nation Risk Index (NRI)

# ## Raw data source:
# https://hazards.fema.gov/nri/data-resources
# 
# - Data Download: County Level > All Counties - County-level detail (Table)

# # Version 1 - 2023 (Crosswalk) + NRI

# # Version 2 - 2013 (Crosswalk) + NRI

# In[20]:


crosswalk_version = 2023


# In[5]:


import sys
sys.path.append('../../scripts')  
import merging_utils
import yaml
import pandas as pd
import os

with open("../../config/preprocessing.yaml", "r") as f:
    preprocessing_config = yaml.safe_load(f)

prefix = preprocessing_config['hazard'][crosswalk_version]['prefix']
fips_key_col = preprocessing_config['hazard'][crosswalk_version]['fips_key_col']
MSA_groupby_col = preprocessing_config['hazard'][crosswalk_version]['MSA_groupby_col']


file_path1 = '../../data/raw/NRI_Table_Counties/NRI_Table_Counties.csv'
file_path2 = preprocessing_config['hazard'][crosswalk_version]['file_path']

df1 = pd.read_csv(file_path1, dtype={'STCOFIPS' : str, MSA_groupby_col: str})
df2 = pd.read_csv(file_path2, dtype={fips_key_col: str})


## column 1
population_loss_equivalent = preprocessing_config['hazard'][crosswalk_version]['population_loss_equivalent']
population_loss_equivalent_cols = [prefix + '_' + col for col in df1.columns if population_loss_equivalent in col]

## column 2
building_loss_equivalent = preprocessing_config['hazard'][crosswalk_version]['building_loss_equivalent']
building_loss_equivalent_cols = [prefix + '_' + col for col in df1.columns if building_loss_equivalent in col]

## column 3
population_exposure = preprocessing_config['hazard'][crosswalk_version]['population_exposure']
population_exposure_cols = [prefix + '_' + col for col in df1.columns if population_exposure in col]

## column 4
building_exposure = preprocessing_config['hazard'][crosswalk_version]['building_exposure']
building_exposure_cols = [prefix + '_' + col for col in df1.columns if building_exposure in col]

## column 5
total_value_cols = preprocessing_config['hazard'][crosswalk_version]['total_value_cols']
total_value_cols = [prefix + '_' + col for col in total_value_cols]

## Can add columns more
additional_col = [prefix + '_' + 'AREA']


# In[8]:


df1.head()


# In[9]:


df2.head()


# # Describe

# In[10]:


df1.shape


# In[11]:


# Extract columns that contain 'EALPE' in their names
ealpe_cols = [col for col in df1.columns if 'EALPE' in col]

# Calculate missing value count and percentage for those columns
ealpe_null_df = pd.DataFrame({
    'Missing Count': df1[ealpe_cols].isnull().sum(),
    'Missing %': df1[ealpe_cols].isnull().mean() * 100
}).sort_values('Missing %', ascending=False)

# View the result
ealpe_null_df


# In[12]:


# Extract columns that contain 'EALB' in their names
ealb_cols = [col for col in df1.columns if 'EALB' in col]

# Calculate missing value count and percentage for those columns
ealb_null_df = pd.DataFrame({
    'Missing Count': df1[ealb_cols].isnull().sum(),
    'Missing %': df1[ealb_cols].isnull().mean() * 100
}).sort_values('Missing %', ascending=False)

# View the result
ealb_null_df


# ## Adding prefix

# In[13]:


print('Before adding prefixes: ' , df1.columns)
df1 = merging_utils.add_prefix_all(df1, prefix=prefix)
print()
print('After adding prefixes: ' , df1.columns)


# ## Merge with join identifiers

# In[14]:


merged_df = pd.merge(left=df1, right=df2, left_on=prefix+'_'+'STCOFIPS', right_on=fips_key_col, how = 'outer')
merged_df[MSA_groupby_col] = merged_df[MSA_groupby_col].astype(str)


# In[15]:


# county level !
merged_df


# ## Define columns to include

# In[16]:


all_relevant_cols = population_loss_equivalent_cols + building_loss_equivalent_cols + population_exposure_cols + building_exposure_cols + total_value_cols + additional_col


# ## Groupby MSA Level

# In[17]:


merged_df_by_msa = merged_df.groupby(MSA_groupby_col, as_index=False)[all_relevant_cols].sum()


# In[18]:


merged_df_by_msa.to_csv(f'../../data/interim/data5_hazard_{crosswalk_version}.csv', index=False)


# In[19]:


# including Metro & Micro -> drop Micro at the Merge_1 notebook.
merged_df_by_msa


# In[ ]:




