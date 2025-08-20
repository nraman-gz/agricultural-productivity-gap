import numpy as np
import pandas as pd
from scipy import optimize as opt

VA_all_data = pd.read_csv('generated data/VA_all_data.csv')

def geary_khamis(data):
    
    diff = 100

    prices = data[['ISO','VA_nom', 'VA_n_nom', 'PPPs_ag', 'PPPs_non_ag']]

    # Initialize "guess" vector of ones for PPP_all and PPP_derived
    prices['PPP_all'] = np.ones(len(prices))
    prices['PPP_derived'] = np.full(len(prices), np.nan)

    # Start iteration
    while diff > 1e-10:

        # Calculate reference prices
        pi_a = np.sum(prices['VA_nom']/ prices['PPP_all']) / np.sum(prices['VA_nom'] / prices['PPPs_ag'])
        pi_n = np.sum(prices['VA_n_nom']/ prices['PPP_all']) / np.sum(prices['VA_n_nom'] / prices['PPPs_non_ag'])

        # Calculate PPP_derived
        for country in prices['ISO']:
            country_row = np.array(prices[prices['ISO'] == country].iloc[0]) # ISO, VA_nom, VA_n_nom, PPPs_ag, PPPs_non_ag, PPP_all, PPP_derived
            prices.loc[prices['ISO'] == country, 'PPP_derived'] = (
            (country_row[1] + country_row[2]) / (pi_a * country_row[1] / country_row[3] + pi_n * country_row[2] / country_row[4])
            )
        
        diff = np.sum(
            np.abs(np.log(prices['PPP_all']) - np.log(prices['PPP_derived']))
            )
        
        prices['PPP_all'] = prices['PPP_derived']

    return prices[['ISO', 'PPP_all']]

geary_khamis(VA_all_data).to_csv('generated data/gk.csv', index=False)