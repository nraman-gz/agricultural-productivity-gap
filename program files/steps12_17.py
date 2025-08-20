import pandas as pd
import numpy as np

# Unify data
gk_PPPs = pd.read_csv('generated data/gk.csv')
VA_all_data = pd.read_csv('generated data/VA_all_data.csv')
df = pd.merge(gk_PPPs, VA_all_data[['ISO', 'VA_nom', 'VA_n_nom', 'VA_aggregate_nom','PPPs_ag', 'PPPs_non_ag']], on='ISO')

# Change base to US
p_US = 10731094000000 / 12895841680146 # Hardcoded until better solution is found
gk_PPPs['PPP_all_fin'] = gk_PPPs['PPP_all'] / gk_PPPs.loc[gk_PPPs['ISO'] == 'USA', 'PPP_all'].item() * p_US

# Calculate sectoral reference prices
pi_a = np.sum(VA_all_data['VA_nom'] / gk_PPPs['PPP_all_fin']) / np.sum(VA_all_data['VA_nom'] / VA_all_data['PPPs_ag'])
pi_n = np.sum(VA_all_data['VA_n_nom'] / gk_PPPs['PPP_all_fin']) / np.sum(VA_all_data['VA_n_nom'] / VA_all_data['PPPs_non_ag'])

# Calculate aggregate VAs
df['cVA_all'] = pi_a * df['VA_nom'] / df['PPPs_ag'] + pi_n * df['VA_n_nom'] / df['PPPs_non_ag']

# Calculate sectoral VAs
df['cVA_ag'] = pi_a * df['VA_nom'] / df['PPPs_ag']
df['cVA_non_ag'] = pi_n * df['VA_n_nom'] / df['PPPs_non_ag']

# Calculate price levels
df['PPP_fin_ag'] = df['VA_nom'] / df['cVA_ag']
df['PPP_fin_non_ag'] = df['VA_n_nom'] / df['cVA_non_ag']

# Derive the aggregate PPP again

df['PPP_fin2_all'] = df['VA_aggregate_nom'] / df['cVA_all'
                                                 ]

df.to_csv('generated data/final_adjusted_VAs.csv', index=False)