import pandas as pd
import numpy as np

# ggdc_data = pd.DataFrame()
# country_list = []
# other_sector_list = []

def retrieve_value(country, sector, value, data):
    return data.loc[(data['countrycode'] == country) &
                         (data['sector'] == sector), value].item()

def retrieve_fisher(country1, country2, sector, data):
    mask = ((data[:,0] == country1) & 
            (data[:,1] == country2) & 
            (data[:,2] == sector))
    return data[mask, 3].item()

def country_to_vec(country, value,data, sector):
    vec = np.array(data[data['countrycode'] == country][value])
    
    if sector == "non_ag":
        return np.delete(vec, 0)
    elif sector == "ag":
        return np.array(vec[0])
    else:
        return vec

def laspeyres(j, h, data, sector):
    VA_h = country_to_vec(h, 'VA_PPP', data, sector)
    PPP_j = country_to_vec(j, 'PPP_sec', data, sector)
    PPP_h = country_to_vec(h, 'PPP_sec', data,sector)

    return PPP_j.dot(VA_h) / PPP_h.dot(VA_h)

def paasche(j,h, data, sector):
    VA_j = country_to_vec(h, 'VA_PPP', data, sector)
    PPP_j = country_to_vec(j, 'PPP_sec', data, sector)
    PPP_h = country_to_vec(h, 'PPP_sec', data, sector)

    return PPP_j.dot(VA_j) / PPP_h.dot(VA_j)

def fisher(j,h, data, sector):
    return np.sqrt(laspeyres(j,h, data, sector) * paasche(j,h, data, sector))

