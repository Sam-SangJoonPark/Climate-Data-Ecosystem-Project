#!/usr/bin/env python
# coding: utf-8

# # Final dataset quality check

# ## Select the version

# In[1]:


criteria_version = 2023


# ### Step 1. Load the data

# In[2]:


import pandas as pd
# Step 0: Get the file path
path = f'../../data/final/final_data_{criteria_version}.csv'

# Step 1: Load the final dataset
final_df = pd.read_csv(path)


# In[3]:


final_df.head()


# ### Step 2. Basic information

# In[4]:


# Step 2: Basic Info
print("\n Dataset shape:\n", final_df.shape)
print("\n Columns:\n", final_df.columns.tolist())
print("\n Data Types:\n", final_df.dtypes)


# ### Step 3. Uniqueness in MSA

# In[5]:


# Step 3: Key Check
key_col = f'Crosswalk{criteria_version}_CBSA Code'
print(f"\n Is '{key_col}' unique?:", final_df[key_col].is_unique)


# ### Step 4. Missing value

# In[6]:


# Step 4: Missing Value Check
missing_count = final_df.isnull().sum()
missing_ratio = final_df.isnull().mean()

missing_summary = pd.DataFrame({
    'Missing Count': missing_count,
    'Missing Ratio (%)': missing_ratio*100
}).sort_values(by='Missing Ratio (%)', ascending=False)

print("\nMissing Value Summary per Column:\n", missing_summary[missing_summary['Missing Count'] > 0])

