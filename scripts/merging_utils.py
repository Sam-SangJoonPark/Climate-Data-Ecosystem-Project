def add_prefix_all(df, prefix):
    return df.rename(columns={col: f"{prefix}_{col}" for col in df.columns})



def get_msa_summary(df, size, agg_method, prefix, cbsa_code, cbsa_title, cbsa_state):
    import pandas as pd
    """
    Filter only Metropolitan Statistical Areas and return MSA summary.
    
    Parameters:
    - df: input dataframe
    - state_mode: 'most_common' or 'concat' to determine how to handle multiple states
    
    Returns:
    - grouped_df: grouped by CBSA Code, with CBSA Title and aggregated State Name
    """

    # Step 1: Filter only Metropolitan Statistical Areas
    if size == 'metro':
        metro_df = df[df[f'{prefix}_Metropolitan/Micropolitan Statistical Area'] == 'Metropolitan Statistical Area']
    if size == 'micro': 
        metro_df = df[df[f'{prefix}_Metropolitan/Micropolitan Statistical Area'] != 'Metropolitan Statistical Area']
  
    # Step 2: Define state aggregation logic
    def aggregate_states(states):
        if agg_method == 'most_common':
            return pd.Series(states).mode()[0]
        elif agg_method == 'concat':
            return ', '.join(sorted(set(states)))
        else:
            raise ValueError("state_mode must be either 'most_common' or 'concat'")

    # Step 3: Group by CBSA Code
    grouped_df = (
        metro_df
        .groupby(cbsa_code)
        .agg({
            cbsa_title: 'first',
            cbsa_state : aggregate_states
        })
        .reset_index()
    )
    
    return grouped_df







    