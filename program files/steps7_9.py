import numpy as np
import pandas as pd
from data_processing import ggdc_data, VA_all_data, country_codes

VA_all_data['p_a'] = VA_all_data['VA_nom'] / VA_all_data ['VA_real']
VA_all_data['p_n'] = VA_all_data['VA_n_nom'] / VA_all_data ['VA_n_real']
VA_all_data['p_agg'] = (VA_all_data['VA_nom'] + VA_all_data['VA_n_nom']) / (VA_all_data ['VA_real'] + VA_all_data ['VA_n_real'])

# resolve differences in country list between VA_all_data and ggdc_data
ggdc_m49_to_iso = {}
GGDC_countries = ggdc_data['countrycode'].unique()


for g in GGDC_countries:
    m = (country_codes[country_codes['Alpha-3 code'] == g]['Numeric code'].item()).strip()
    ggdc_m49_to_iso[g] = m

VA_map = {v:k for k,v in ggdc_m49_to_iso.items()}

ggdc_data['m49'] = ggdc_data['countrycode'].map(ggdc_m49_to_iso)
VA_all_data['ISO'] = VA_all_data['CountryID'].map(VA_map).fillna(np.nan)
VA_all_data = VA_all_data.dropna()

GEKS = pd.read_csv('generated data/geks.csv')

# Create dictionaries for each sector
sectors = ['ag', 'non_ag', 'aggregate']
country_to_GEKS = {
    sector: GEKS[GEKS['sector'] == sector].set_index('country1')['GEKS_index_standardized'].to_dict()
    for sector in sectors
}

# Add GEKS indices for each sector to VA_all_data
for sector in sectors:
    VA_all_data[f'GEKS {sector} index'] = VA_all_data['ISO'].map(country_to_GEKS[sector])

# Calculate PPPs using USA prices as base
usa_mask = VA_all_data['ISO'] == 'USA'
price_cols = {'ag': 'p_a', 'non_ag': 'p_n', 'aggregate': 'p_agg'}

for sector, price_col in price_cols.items():
    usa_price = VA_all_data.loc[usa_mask, price_col].item()
    VA_all_data[f'PPPs_{sector}'] = VA_all_data[f'GEKS {sector} index'] * usa_price

# Calculate PPP-adjusted values
VA_all_data['VA_ag_PPP'] = VA_all_data['VA_nom'] / VA_all_data['PPPs_ag']
VA_all_data['VA_non_ag_PPP'] = VA_all_data['VA_n_nom'] / VA_all_data['PPPs_non_ag']
VA_all_data['VA_agg_PPP'] = (VA_all_data['VA_nom'] + VA_all_data['VA_n_nom']) / VA_all_data['PPPs_aggregate']

VA_all_data.to_csv('generated data/VA_all_data.csv', index=False)