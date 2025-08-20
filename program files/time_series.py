import pandas as pd
import numpy as np
from data_processing import VA_time_series
from steps12_17 import df

# Add year to df (2005)
df['Year'] = 2005

# Need to make countries from VA_time_series and previous steps agree
from steps7_9 import VA_map
VA_map = {float(key): value for key, value in VA_map.items()} # Convert to floats to be used with CountryID values
VA_time_series['ISO'] = VA_time_series['CountryID'].map(VA_map).fillna(np.nan)
VA_time_series = VA_time_series.dropna()
VA_time_series = VA_time_series.drop(['CountryID', 'Country', 'IndicatorName'], axis=1)

# Compute sectoral prices for all years
VA_time_series['p_a_t'] = VA_time_series['VA_nom']/VA_time_series['VA_real']
VA_time_series['p_n_t'] = VA_time_series['VA_n_nom']/VA_time_series['VA_n_real']
VA_time_series['p_t'] = VA_time_series['VA_aggregate_nom']/VA_time_series['VA_aggregate_real']

deflated = pd.DataFrame()

# Create lists for each column
countries = []
years = []
ppp_at_na = []
ppp_nt_na = []
ppp_t_na = []
rva_a_t = []
rva_n_t = []
rva_t = []

# Get unique countries
unique_countries = VA_time_series['ISO'].unique()
years_range = range(1970, 2024)

# Iterate through each country and year
for country in unique_countries:
    base_ppp_ag = df.loc[df['ISO'] == country, 'PPP_fin_ag'].iloc[0]
    base_ppp_non_ag = df.loc[df['ISO'] == country, 'PPP_fin_non_ag'].iloc[0]
    base_ppp_aggregate = df.loc[df['ISO'] == country, 'PPP_fin2_all'].iloc[0]
    
    country_data = VA_time_series[VA_time_series['ISO'] == country]
    p_at_2005 = country_data.loc[country_data['Year'] == 2005, 'p_a_t'].iloc[0]
    p_nt_2005 = country_data.loc[country_data['Year'] == 2005, 'p_n_t'].iloc[0]
    p_t_2005 = country_data.loc[country_data['Year'] == 2005, 'p_t'].iloc[0]
    
    for year in years_range:
        try:
            p_at = country_data.loc[country_data['Year'] == year, 'p_a_t'].iloc[0]
            p_nt = country_data.loc[country_data['Year'] == year, 'p_n_t'].iloc[0]
            p_t = country_data.loc[country_data['Year'] == year, 'p_t'].iloc[0]
            
            countries.append(country)
            years.append(year)
            ppp_at_na.append(base_ppp_ag * p_at / p_at_2005)
            ppp_nt_na.append(base_ppp_non_ag * p_nt / p_nt_2005)
            ppp_t_na.append(base_ppp_aggregate * p_t / p_t_2005)

            rva_a_t.append(country_data.loc[country_data['Year'] == year, 'VA_nom'].iloc[0] / (base_ppp_ag * p_at / p_at_2005))
            rva_n_t.append(country_data.loc[country_data['Year'] == year, 'VA_n_nom'].iloc[0] / (base_ppp_non_ag * p_nt / p_nt_2005))
            rva_t.append(country_data.loc[country_data['Year'] == year, 'VA_aggregate_nom'].iloc[0] / (base_ppp_aggregate * p_t / p_t_2005))
        except IndexError:
            continue



# Create the deflated dataframe
deflated = pd.DataFrame({
    'ISO': countries,
    'Year': years,
    'PPP_a_t_na': ppp_at_na,
    'PPP_n_t_na': ppp_nt_na,
    'PPP_t_na': ppp_t_na,
    'rVA_a_t': rva_a_t,
    'rVA_n_t': rva_n_t,
    'rVA_t' : rva_t
})

deflated.to_csv('generated data/deflated.csv', index=False)