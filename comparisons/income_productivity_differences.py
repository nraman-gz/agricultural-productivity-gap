import pandas as pd
import matplotlib.pyplot as plt
from employment_data import merged_data

# Sort countries by VA_i_PPP in descending order
sorted_data = merged_data.sort_values('VA_i_PPP', ascending=False)

# Display sorted list of countries
# print("\nCountries sorted by VA_i_PPP (highest to lowest):")
# print(sorted_data[['ISO', 'VA_i_PPP']])

# Calculate averages of top 5 and bottom 5
top_5_avg = sorted_data.head(5)['VA_i_PPP'].mean()
bottom_5_avg = sorted_data.tail(5)['VA_i_PPP'].mean()

top_5_ag_prod = sorted_data.head(5)['VA_pw_agr_PPP'].mean()
bottom_5_ag_prod = sorted_data.tail(5)['VA_pw_agr_PPP'].mean()

top_5_non_ag_prod = sorted_data.head(5)['VA_pw_non_agr_PPP'].mean()
bottom_5_non_ag_prod = sorted_data.tail(5)['VA_pw_non_agr_PPP'].mean()

# Income ratios
income_ratio = top_5_avg / bottom_5_avg
ag_prod_ratio = top_5_ag_prod / bottom_5_ag_prod
non_ag_prod_ratio = top_5_non_ag_prod / bottom_5_non_ag_prod
print(income_ratio, ag_prod_ratio, non_ag_prod_ratio)

# Sectoral emplyment shares
top_5_ag_emp_share = sorted_data.head(5)['agr_emp_share'].mean()
bottom_5_ag_emp_share = sorted_data.tail(5)['agr_emp_share'].mean()

# Create bar chart
ratios = [ag_prod_ratio, non_ag_prod_ratio, income_ratio]
labels = ['Agriculture', 'Non-Agriculture', 'Aggregate']

if __name__ == "__main__":
    plt.rcParams['font.family'] = 'Palatino'
    plt.figure(figsize=(8, 4))
    plt.bar(labels, ratios, color=['skyblue', 'lightgreen', 'salmon'], width=0.4)
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 12)
    plt.ylabel('Ratio', fontsize = 16)
    # plt.figtext(0.5, 0.01, 'Ratio of Sectoral Productivity of Top 5 to Bottom 5 Countries, Ranked by Value Added per Worker', ha='center', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout(pad = 3.0)

    plt.savefig("figures/sectoral_prod_top5_bottom5.pdf")
    # plt.savefig("figures/sectoral_prod_top5_bottom5.png", transparent=True)

    # plt.show()
