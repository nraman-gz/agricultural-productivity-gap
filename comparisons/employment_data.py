import pandas as pd

# It is not possible to load the ILO data directly from URL due to restrictions,therefore it must be downloaded manually
# The filters are all regions, all reference areas, "total" for sex, and
# aggregate total + aggregate agriculture for economic activity, year 2005
ILO_filename = "EMP_2EMP_SEX_ECO_NB_A-filtered-2025-08-13.csv"
ILO_data = pd.read_csv(ILO_filename)

# Pivot data to have sector as columns
ILO_data = ILO_data.pivot_table(
    index=['ref_area', 'time'], 
    columns='classif1', 
    values='obs_value').reset_index()

ILO_data.rename(columns={
    'ref_area': 'ISO',
    'time': 'Year',
    'ECO_AGGREGATE_AGR': 'agr_emp',
    'ECO_AGGREGATE_TOTAL': 'total_emp',
}, inplace=True)

# ILO data is in thousands, convert to single units
ILO_data['agr_emp'] = 1000 * ILO_data['agr_emp']
ILO_data['total_emp'] = 1000 * ILO_data['total_emp']

# Compute non-agricultural employment numbers
ILO_data['non_agr_emp'] = ILO_data['total_emp'] - ILO_data['agr_emp']

VA_data = pd.read_csv("generated data/final_adjusted_VAs.csv")

# Drop countries that are not present in VA_data
valid_countries = VA_data['ISO'].unique()
ILO_data = ILO_data[ILO_data['ISO'].isin(valid_countries)]


# Calculate employment shares
ILO_data['agr_emp_share'] = ILO_data['agr_emp'] / ILO_data['total_emp']
ILO_data['non_agr_emp_share'] = ILO_data['non_agr_emp'] / ILO_data['total_emp']

merged_data = pd.merge(VA_data, ILO_data, on='ISO', how='left')

# PPP adjusted income per capita
merged_data['VA_i_PPP'] = merged_data['cVA_all'] / merged_data['total_emp']

# Nominal VA per worker
merged_data['VA_pw_agr'] = merged_data['VA_nom'] / merged_data['agr_emp']
merged_data['VA_pw_non_agr'] = merged_data['VA_n_nom'] / merged_data['non_agr_emp']
merged_data['VA_pw'] = merged_data['VA_aggregate_nom'] / merged_data['total_emp']

# PPP sectoral VA per worker
merged_data['VA_pw_agr_PPP'] = merged_data['cVA_ag'] / merged_data['agr_emp']
merged_data['VA_pw_non_agr_PPP'] = merged_data['cVA_non_ag'] / merged_data['non_agr_emp']
merged_data['VA_pw_PPP'] = merged_data['cVA_all'] / merged_data['total_emp']
