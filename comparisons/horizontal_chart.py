import pandas as pd
import matplotlib.pyplot as plt
from income_productivity_differences import sorted_data

top_5 = sorted_data.head(5)
bottom_5 = sorted_data.tail(5)

# Combine top and bottom 5
combined = pd.concat([top_5, bottom_5])
countries = combined['ISO']
values = combined['VA_pw_PPP']

# Plot
plt.rcParams['font.family'] = 'Palatino'
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(countries, values, color='skyblue')

# Add value labels
for bar in bars:
    width = bar.get_width()
    # ax.text(width + 1, bar.get_y() + bar.get_height()/2,
    #         f"${width:.1f}", va='center', fontsize=14)

# Styling
ax.set_xlabel('PPP Adjusted Dollars ($)', fontsize=18)
ax.invert_yaxis()  # Highest value at top
plt.yticks(fontsize=18)
plt.xticks(fontsize=18)

# # Add horizontal padding to the right
# max_value = max(values)
# ax.set_xlim([0, max_value + 20])

plt.savefig("figures/horizontal_chart.pdf")

plt.tight_layout()
plt.show()
