import pandas as pd
import numpy as np
import cnemc_calculator

from importlib import reload

## calculate_daily_aqi
cnemc_calculator = reload(cnemc_calculator)

data = pd.read_excel('data/审核后点位日均值.xlsx', header=0, index_col=[3,4], na_values=[-1,-99], sheetname='2016')
column_names = ['SO2', 'NO2', 'PM10', 'CO(mg/m3)', 'O3', 'O3-8h','PM2.5']
data[column_names] = data[column_names].convert_objects(convert_numeric=True)
data['CO(mg/m3)']=cnemc_calculator.functions.sci_round(data['CO(mg/m3)'])
data_aqi = cnemc_calculator.calculate_daily_aqi(data, column_names)
data_aqi.to_excel('data/aqi.xlsx')
# pd.read_excel('data/iAQI限值.xlsx', index_col=0)

comp = pd.concat((data['AQI'], data_aqi['AQI']),axis=1)