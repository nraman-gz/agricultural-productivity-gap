import pandas as pd
import matplotlib.pyplot as plt
from employment_data import merged_data

# Compute value added shares for plotting
merged_data['VA_pw_agr_share'] = merged_data['VA_pw_agr'] / merged_data['VA_pw']
merged_data['VA_pw_non_agr_share'] = merged_data['VA_pw_non_agr'] / merged_data['VA_pw']

print(min(merged_data['VA_pw_agr_share']))


# Assuming 'merged_data' is already defined and contains the necessary columns
# Create the scatter plot
plt.rcParams['font.family'] = 'Palatino'
fig, ax = plt.subplots(figsize=(10, 5))

for i, row in merged_data.iterrows():
    plt.text(row['VA_pw_agr_share'], row['VA_pw_non_agr_share'], row['ISO'], fontsize=12, ha='center', va='center')

# Add a dashed line representing VA_pw_agr = VA_pw_non_agr

# min_val = min(merged_data['VA_pw_agr_share'].min(), merged_data['VA_pw_non_agr_share'].min())
# max_val = max(merged_data['VA_pw_agr_share'].max(), merged_data['VA_pw_non_agr_share'].max())
ax.plot([merged_data['VA_pw_agr_share'].min(), merged_data['VA_pw_agr_share'].max()], [merged_data['VA_pw_non_agr_share'].min(), merged_data['VA_pw_non_agr_share'].max()], linestyle='--', color='gray')


# Labeling the plot
plt.xlabel('Agricultural', fontsize = 18)
plt.ylabel('Non-Agricultural', fontsize = 18)
plt.xticks(fontsize = 16)
plt.yticks(fontsize = 16)
plt.tight_layout(pad = 2.0)

plt.savefig('figures/nominalAPG.pdf')



