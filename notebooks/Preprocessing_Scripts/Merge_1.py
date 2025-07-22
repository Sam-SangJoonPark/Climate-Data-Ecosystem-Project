#!/usr/bin/env python
# coding: utf-8

# ## Merging

# ## Tweaks: 
# - 2023 cross walk
# - 2013 cross walk

# In[1]:


crosswalk_version = 2023


# In[2]:


import yaml
import pandas as pd

# Step 1: Load YAML
with open("../../config/merging.yaml", "r") as f:
    config = yaml.safe_load(f)

# Step 2: Select version and extract file names
file_list = config[crosswalk_version]['files']
join_keys = config[crosswalk_version]['join_keys']

# Step 3: Define data folder path
data_path = "../../data/interim/"


# In[3]:


# Step 4: Load each CSV using the paths from the config
criteria_df = pd.read_csv(data_path + file_list["criteria"])
hazard_df   = pd.read_csv(data_path + file_list["hazard"])
migration_df= pd.read_csv(data_path + file_list["migration"])
housing_df  = pd.read_csv(data_path + file_list["housing"])


# In[4]:


join_keys


# In[5]:


criteria_df.head(3)


# In[6]:


hazard_df.head(3)


# In[7]:


migration_df.head(3)


# In[8]:


housing_df.head(3)


# In[9]:


# Step 1 : Already done loading datasets.

# Step 2: Set base
combined_df = criteria_df.copy()

# Step 3: Merge datasets
combined_df = combined_df.merge(
    hazard_df,
    how='left',
    left_on=join_keys['criteria'],
    right_on=join_keys['hazard'],
    suffixes=('', '_hazard')
)

combined_df = combined_df.merge(
    migration_df,
    how='left',
    left_on=join_keys['criteria'],
    right_on=join_keys['migration'],
    suffixes=('', '_migration')
)

combined_df = combined_df.merge(
    housing_df,
    how='left',
    left_on=join_keys['criteria'],
    right_on=join_keys['housing'],
    suffixes=('', '_housing')
)

# Step 4: Drop only non-criteria join keys
redundant_keys = [
    join_keys['hazard'],
    join_keys['migration'],
    join_keys['housing']
]
redundant_keys = [key for key in redundant_keys if key != join_keys['criteria']]

combined_df.drop(columns=redundant_keys, inplace=True, errors='ignore')

# Step 5: Reorder to put CBSA code first
cbsa_col = join_keys['criteria']
cols = combined_df.columns.tolist()
combined_df = combined_df[[cbsa_col] + [col for col in cols if col != cbsa_col]]

# Step 6: Preview
combined_df.head()


# In[10]:


combined_df.to_csv(f'../../data/final/final_data_{crosswalk_version}.csv', index=False)


# In[11]:


combined_df

