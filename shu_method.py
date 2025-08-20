import pandas as pd
import math
import numpy as np
from utils import laspeyres, paasche, fisher, retrieve_fisher

# print(GO_all_data['Year'].unique())

# fao_intl = pd.read_csv("datasets/FAOSTAT_intl.csv", usecols=[2,3,9,11])
# fao_intl.rename(columns={'Value':'GO_PPP'}, inplace=True)

# fao_con = pd.read_csv("datasets/FAOSTAT_constant.csv", usecols= [2,3,9,11])
# fao_con.rename(columns={'Value':'GO_real'}, inplace=True)

# fao_cur = pd.read_csv("datasets/FAOSTAT_current.csv", usecols= [2,3,9,11])
# fao_cur.rename(columns={'Value':'GO_nom'}, inplace=True)

# countries = set(fao_intl['Area'].unique())
# years = set(fao_intl['Year'].unique())
# # len(fao_intl['Year'].unique())
# # 54

# GO_all_data = fao_intl.merge(fao_con, how="outer")
# GO_all_data = GO_all_data.merge(fao_cur, how = "outer")
# GO_all_data['PPP_a'] = GO_all_data['GO_nom'] / GO_all_data['GO_PPP']

unsd_constant = pd.read_excel("datasets/UNSD_AMA_constant.xlsx", sheet_name=0,
                                        skiprows=[0,1])
unsd_current = pd.read_excel("datasets/UNSD_AMA_current.xlsx", sheet_name=0,
                                        skiprows=[0,1])

unsd_constant = unsd_constant.melt(id_vars=['CountryID','Country','IndicatorName'],
                   var_name='Year', value_name='VA_real')
unsd_current = unsd_current.melt(id_vars=['CountryID','Country','IndicatorName'],
                   var_name='Year', value_name='VA_nom')
# unsd_current.to_csv('unsd_current.csv')

VA_all_data = unsd_constant.merge(unsd_current, how= "outer")

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
VA_all_data.to_csv('VA_all_data.csv')

ggdc_data = pd.read_excel("datasets/GGDC_PLD_2023.xlsx", sheet_name=1)
ggdc_data['VA_PPP'] = ggdc_data['VA']/ggdc_data['PPP_va']
ggdc_data['PPP_sec'] = ggdc_data['PPP_va']/ggdc_data['xr']
ggdc_data = ggdc_data.drop(ggdc_data.columns[[4,5,9]], axis=1)

ggdc_data = ggdc_data[ggdc_data['year'] == 2005]
ggdc_data.to_csv('ggdc.csv')

country_list = ggdc_data['countrycode'].unique()
other_sector_list = np.delete(ggdc_data['sector'].unique(), 0)
# print(other_sector_list)

GGDC_countries = ggdc_data['countrycode'].unique()
UNSD_countries = VA_all_data['CountryID'].unique()
UNSD_countries[np.isnan(UNSD_countries)] = 492
UNSD_countries = np.array([str(i) for i in UNSD_countries])
country_codes = pd.read_csv('countries_codes_and_coordinates.csv')
country_codes.replace('"', '', inplace= True, regex=True)
country_codes = country_codes[['Alpha-3 code','Numeric code']]
country_codes['Alpha-3 code'] = country_codes['Alpha-3 code'].str.strip()

mask = np.isin(UNSD_countries, np.array(country_codes['Numeric code']))

fisher_indices = []

for i in range(len(country_list)):
    for j in range(i+1, len(country_list)):
        country_i = country_list[i]
        country_j = country_list[j]
        f_ij = fisher(country_i, country_j, data=ggdc_data)
        f_ji = fisher(country_j, country_i, data=ggdc_data)

        f_ij_a = fisher(country_i, country_j, data=ggdc_data, non_ag= False)
        f_ji_a = fisher(country_j, country_i, data=ggdc_data, non_ag= False)

        if np.isnan(f_ij) or np.isnan(f_ji):
            print("Error, fisher index is 0")
        
        fisher_indices.append({
            'country1': country_i,
            'country2': country_j,
            'fisher_index_non_ag': f_ij,
            'fisher_index_ag': f_ij_a
            })

        fisher_indices.append({
            'country2': country_i,
            'country1': country_j,
            'fisher_index_non_ag': f_ji,
            'fisher_index_ag': f_ji_a
            })

fisher_indices = pd.DataFrame(fisher_indices)
fisher_indices.to_csv('fishers.csv')


# # fisher_indices = pd.read_csv('fishers.csv')
to_USA_fishers = np.array(fisher_indices.loc[fisher_indices['country2'] == 'USA'])

countries_minus_USA = np.delete(country_list, np.where(country_list == 'USA'))

geks = []

for j in range(len(country_list)):
    country_j = country_list[j]
    j_fishers = np.array(fisher_indices.loc[fisher_indices['country1'] == country_j])
    h_countries = np.delete(countries_minus_USA, np.where(countries_minus_USA == country_j))
    C = np.size(h_countries)
    expon = 1 / C
    temp = []
    for h in h_countries:
        num = np.power(
            retrieve_fisher(country_j, h, j_fishers) * retrieve_fisher(h, 'USA', to_USA_fishers),
            expon)
        temp.append(num)
    geks_j = np.prod(np.array(temp))
    geks.append({'country1': country_j,
                'country2': 'USA',
                'GEKS_index': geks_j})

geks_indices = pd.DataFrame(geks)

# geks = pd.read_csv('GEKS.csv')
# geks['GEKS_index_standardized'] = geks['GEKS_index']/ (geks.loc[(geks['country1'] == 'USA') &
#                                                                 (geks['country2'] == 'USA'), 'GEKS_index'].item() )
# geks.to_csv('GEKS.csv')

VA_all_data = VA_all_data[VA_all_data['Year'] == 2005]
VA_all_data = VA_all_data.dropna()
VA_all_data['CountryID'] = VA_all_data['CountryID'].astype(int).astype(str)

VA_all_data['p_a'] = VA_all_data['VA_nom'] / VA_all_data ['VA_real']
VA_all_data['p_n'] = VA_all_data['VA_n_nom'] / VA_all_data ['VA_n_real']
VA_all_data['p_agg'] = (VA_all_data['VA_nom'] + VA_all_data['VA_n_nom']) / (VA_all_data ['VA_real'] + VA_all_data ['VA_n_real'])



ggdc_m49_to_iso = {}

for g in GGDC_countries:
    m = (country_codes[country_codes['Alpha-3 code'] == g]['Numeric code'].item()).strip()
    ggdc_m49_to_iso[g] = m

VA_map = {v:k for k,v in ggdc_m49_to_iso.items()}

ggdc_data['m49'] = ggdc_data['countrycode'].map(ggdc_m49_to_iso)
VA_all_data['ISO'] = VA_all_data['CountryID'].map(VA_map).fillna(np.nan)
ggdc_data.to_csv('ggdc.csv')
VA_all_data = VA_all_data.dropna()

GEKS = pd.read_csv('GEKS.csv')
GEKS_ag = pd.read_csv('GEKS_ag.csv')
country_to_GEKS_ag = GEKS_ag.set_index('country1')['GEKS_index_standardized'].to_dict()
country_to_GEKS = GEKS.set_index('country1')['GEKS_index_standardized'].to_dict()
print(country_to_GEKS_ag)

VA_all_data['GEKS non-ag index'] = VA_all_data['ISO'].map(country_to_GEKS)
VA_all_data['GEKS ag index'] = VA_all_data['ISO'].map(country_to_GEKS_ag)


VA_all_data['PPPs_ag'] = VA_all_data['GEKS ag index'] * VA_all_data[VA_all_data['ISO'] == 'USA']['p_a'].item()
VA_all_data['PPPs_non_ag'] = VA_all_data['GEKS non-ag index'] * VA_all_data[VA_all_data['ISO'] == 'USA']['p_n'].item()

VA_all_data['VA_ag_PPP'] = VA_all_data['VA_nom'] / VA_all_data['PPPs_ag']
VA_all_data['VA_non_ag_PPP'] = VA_all_data['VA_n_nom'] / VA_all_data['PPPs_non_ag']

VA_all_data.to_csv('VA_all_data.csv')


