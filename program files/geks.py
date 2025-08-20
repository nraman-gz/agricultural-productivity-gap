import pandas as pd
import numpy as np
from data_processing import country_list
from utils import retrieve_fisher

fisher_indices = pd.read_csv('/Users/nikhil/Documents/APG Data/generated data/fishers.csv')

to_USA_fishers = np.array(fisher_indices.loc[fisher_indices['country2'] == 'USA'])

countries_minus_USA = np.delete(country_list, np.where(country_list == 'USA'))

geks = []

for sector in ['ag', 'non_ag', 'aggregate']:
    for i in range(len(country_list)):
        country_i = country_list[i]
        i_fishers = np.array(fisher_indices.loc[(fisher_indices['country1'] == country_i) & (fisher_indices['sector'] == sector)])
        h_countries = np.delete(countries_minus_USA, np.where(countries_minus_USA == country_i))
        C = np.size(h_countries)
        expon = 1 / C
        temp = []
        for h in h_countries:
            num = np.power(
                retrieve_fisher(country_i, h, sector, i_fishers) * retrieve_fisher(h, 'USA', sector,to_USA_fishers),
                expon)
            temp.append(num)
        geks_i = np.prod(np.array(temp))
        geks.append({'country1': country_i,
                     'country2': 'USA',
                     'sector': sector,
                     'GEKS_index': geks_i})
            
df_geks = pd.DataFrame(geks)

df_geks['GEKS_index_standardized'] = None
for sector in ['ag', 'non_ag', 'aggregate']:
    mask = df_geks['sector'] == sector
    denominator = df_geks.loc[(df_geks['country1'] == 'USA') & (df_geks['country2'] == 'USA') & (df_geks['sector'] == sector), 'GEKS_index'].item()
    df_geks.loc[mask, 'GEKS_index_standardized'] = df_geks.loc[mask, 'GEKS_index'] / denominator


output_path = '/Users/nikhil/Documents/APG Data/generated data/geks.csv'
df_geks.to_csv(output_path, index=False)