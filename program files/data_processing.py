import pandas as pd
import numpy as np
from load_merge_data import VA_all_data, ggdc_data, country_codes

VA_all_data_ag = VA_all_data[
    VA_all_data['IndicatorName'] == 'Agriculture, hunting, forestry, fishing (ISIC A-B)'
    ]

VA_all_data_n = VA_all_data[
    VA_all_data['IndicatorName'].isin(['Mining, Manufacturing, Utilities (ISIC C-E)', 
                                     'Construction (ISIC F)', 'Wholesale, retail trade, restaurants and hotels (ISIC G-H)',
                                     'Transport, storage and communication (ISIC I)', 'Other Activities (ISIC J-P)'])
    ]

VA_all_data_n = VA_all_data_n.groupby(['Country', 'Year'], as_index= False)[['VA_nom', 'VA_real']].sum()
VA_all_data_n.rename(columns= {'VA_nom':'VA_n_nom','VA_real':'VA_n_real'}, inplace=True)
VA_all_data = VA_all_data_ag.merge(VA_all_data_n, how='outer')
VA_all_data['VA_aggregate_nom'] = VA_all_data['VA_nom'] + VA_all_data['VA_n_nom']
VA_all_data['VA_aggregate_real'] = VA_all_data['VA_real'] + VA_all_data['VA_n_real']
VA_time_series = VA_all_data # Save this for time series section
VA_all_data = VA_all_data[VA_all_data['Year'] == 2005]
VA_all_data = VA_all_data.dropna()
VA_all_data['CountryID'] = VA_all_data['CountryID'].astype(int).astype(str)

ggdc_data['VA_PPP'] = ggdc_data['VA']/ggdc_data['PPP_va']
ggdc_data['PPP_sec'] = ggdc_data['PPP_va']/ggdc_data['xr']
ggdc_data = ggdc_data.drop(ggdc_data.columns[[4,5,9]], axis=1)

ggdc_data = ggdc_data[ggdc_data['year'] == 2005]

country_list = ggdc_data['countrycode'].unique()
other_sector_list = np.delete(ggdc_data['sector'].unique(), 0)

country_codes.replace('"', '', inplace= True, regex=True)
country_codes = country_codes[['Alpha-3 code','Numeric code']].dropna()
country_codes['Alpha-3 code'] = country_codes['Alpha-3 code'].astype(str).str.strip()

VA_time_series.to_csv('generated data/VA_time_series.csv', index=False)