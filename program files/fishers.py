import pandas as pd
import numpy as np
from data_processing import ggdc_data, country_list
from utils import fisher

fisher_indices = []

for sector in ['ag', 'non_ag', 'aggregate']:
    for i in range(len(country_list)):
        for j in range(i+1, len(country_list)):
            country_i = country_list[i]
            country_j = country_list[j]
            f_ij = fisher(country_i, country_j, data=ggdc_data, sector=sector)
            f_ji = fisher(country_j, country_i, data=ggdc_data, sector=sector)

            fisher_indices.append({
                'country1': country_i,
                'country2': country_j,
                'sector': sector,
                'fisher_index': f_ij
            })

            fisher_indices.append({
                'country2': country_i,
                'country1': country_j,
                'sector': sector,
                'fisher_index': f_ji
            })


df_fisher = pd.DataFrame(fisher_indices)
output_path = '/Users/nikhil/Documents/APG Data/generated data/fishers.csv'
df_fisher.to_csv(output_path, index=False)
