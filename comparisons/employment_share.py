import pandas as pd
import matplotlib.pyplot as plt
from income_productivity_differences import top_5_ag_emp_share, bottom_5_ag_emp_share

# Calculate non-agricultural employment share
top_5_non_ag_emp_share = 1 - top_5_ag_emp_share
bottom_5_non_ag_emp_share = 1 - bottom_5_ag_emp_share

plt.rcParams['font.family'] = 'Palatino'

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Pie chart for top 5
axes[0].pie([top_5_ag_emp_share, top_5_non_ag_emp_share],
            # labels=['Agricultural', 'Non-Agricultural'],
            autopct='%1.1f%%',
            colors=['lightgreen', 'lightblue'],
            startangle=90,
            textprops = {'fontsize': 20})
axes[0].set_title('Top 5 Countries', fontsize = 24)

# Pie chart for bottom 5
axes[1].pie([bottom_5_ag_emp_share, bottom_5_non_ag_emp_share],
            # labels=['Agricultural', 'Non-Agricultural'],
            autopct='%1.1f%%',
            colors=['lightgreen', 'lightblue'],
            startangle=90,
            textprops = {'fontsize': 20})
axes[1].set_title('Bottom 5 Countries', fontsize = 24)

fig.legend(['Agricultural', 'Non-Agricultural'], loc='lower center', fontsize=24, ncol=2)

plt.savefig("figures/employment_share_top5_bottom5.pdf")

plt.tight_layout(pad = 3.0)
plt.show()



