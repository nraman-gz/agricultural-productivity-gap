import pandas as pd
import matplotlib.pyplot as plt 

data = pd.read_csv('generated data/deflated.csv')

# Load ILO time series data
ILO_time_series_filename = 'EMP_2EMP_SEX_ECO_NB_A-filtered-2025-08-16.csv'
ILO_time_series = pd.read_csv(ILO_time_series_filename)

# Pivot data to have sector as columns
ILO_time_series = ILO_time_series.pivot_table(
    index=['ref_area', 'time'], 
    columns='classif1', 
    values='obs_value').reset_index()

ILO_time_series.rename(columns={
    'ref_area': 'ISO',
    'time': 'Year',
    'ECO_AGGREGATE_AGR': 'agr_emp',
    'ECO_AGGREGATE_TOTAL': 'total_emp',
}, inplace=True)

# ILO data is in thousands, convert to single units
ILO_time_series['agr_emp'] = 1000 * ILO_time_series['agr_emp']
ILO_time_series['total_emp'] = 1000 * ILO_time_series['total_emp']

# Compute non-agricultural employment numbers
ILO_time_series['non_agr_emp'] = ILO_time_series['total_emp'] - ILO_time_series['agr_emp']

# Drop countries that are not present in VA_data
valid_countries = data['ISO'].unique()
years = ILO_time_series['Year'].unique()
ILO_time_series = ILO_time_series[ILO_time_series['ISO'].isin(valid_countries)]
data = data[data['Year'].isin(years)]

# Calculate employment shares
ILO_time_series['agr_emp_share'] = ILO_time_series['agr_emp'] / ILO_time_series['total_emp']
ILO_time_series['non_agr_emp_share'] = ILO_time_series['non_agr_emp'] / ILO_time_series['total_emp']

merged_data = pd.merge(data, ILO_time_series, on=['ISO', 'Year'], how='left')
merged_data['APG'] = (merged_data['rVA_n_t'] / merged_data['non_agr_emp']) / (merged_data['rVA_a_t'] / merged_data['agr_emp'])

# Define the countries to plot
countries = ['IND', 'CHN']

# Create subplots for each country
plt.rcParams['font.family'] = 'Palatino'
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 5), sharex=True)
axes = axes.flatten()

for i, country in enumerate(countries):
    ax1 = axes[i]
    country_data = merged_data[merged_data['ISO'] == country]

    # Plot APG on left y-axis
    line1, = ax1.plot(country_data['Year'], country_data['APG'], color='skyblue', label='APG')
    ax1.tick_params(axis='x', labelsize=14)
    ax1.set_xlabel(country, fontsize=18)
    ax1.set_ylabel('Real APG', fontsize = 14)
    # ax1.set_title(country)

    # Create second y-axis for agr_emp_share
    ax2 = ax1.twinx()
    line2, = ax2.plot(country_data['Year'], country_data['agr_emp_share'], color='lightgreen', linestyle = 'dashed',label='Agr. Employment Share')
    ax2.set_ylabel('Agricultural Employment Share (%)', fontsize = 14)
    # ax1.set_title(country)

    ax1.set_xlabel('Year', fontsize = 18)
    
    lines = [line1, line2]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='upper right')


plt.tight_layout()

plt.savefig('figures/time_series.pdf')

# plt.show()



