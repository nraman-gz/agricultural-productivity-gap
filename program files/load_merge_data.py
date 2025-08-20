import pandas as pd
import numpy as np

url_unsd_ama_constant = "https://unstats.un.org/unsd/amaapi/api/file/6"
url_unsd_ama_current = "https://unstats.un.org/unsd/amaapi/api/file/2"
url_ggdc = "https://dataverse.nl/api/access/datafile/383800"

unsd_constant = pd.read_excel(url_unsd_ama_constant, sheet_name=0, skiprows=[0,1])
unsd_current = pd.read_excel(url_unsd_ama_current, sheet_name=0, skiprows=[0,1])
ggdc_data = pd.read_excel(url_ggdc, sheet_name=1)

unsd_constant = unsd_constant.melt(id_vars=['CountryID','Country','IndicatorName'], var_name='Year', value_name='VA_real')
unsd_current = unsd_current.melt(id_vars=['CountryID','Country','IndicatorName'], var_name='Year', value_name='VA_nom')

VA_all_data = unsd_constant.merge(unsd_current, how= "outer")

country_codes = pd.read_csv('countries_codes_and_coordinates.csv')