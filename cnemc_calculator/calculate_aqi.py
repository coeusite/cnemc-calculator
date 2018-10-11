import numpy as np
import pandas as pd

from .constants import *
from .functions import *

def calculate_daily_aqi(data, column_names):
    ''' calculate_daily_aqi funcion
    
    data: a pandas dataframe
    column_names: names of factor columns insequence of ['SO2', 'NO2', 'PM10', 'CO', 'O3', 'O3_8H', 'PM_25']
    
    iAQI = 501 means it exceeds the upper limit
    
    '''
    return calculate_aqi(data, column_names, version='HJ663-2012')

def calculate_hourly_aqi(data, column_names):
    ''' calculate_daily_aqi funcion
    
    data: a pandas dataframe
    column_names: names of factor columns insequence of ['SO2', 'NO2', 'PM10', 'CO', 'O3', 'PM_25']
    
    iAQI = 501 means it exceeds the upper limit
    
    '''
    return calculate_aqi(data, column_names, version='HJ663-2012@H')

def calculate_aqi(data, column_names, version='HJ663-2012'):
    ''' calculate_daily_aqi funcion
    
    data: a pandas dataframe
    column_names: names of factor columns insequence of ['SO2', 'NO2', 'PM10', 'CO', 'O3', 'O3_8H', 'PM_25']
    
    iAQI = 501 means it exceeds the upper limit
    
    '''
    tmp_data = data[column_names].convert_objects(convert_numeric=True)
    if version[-2:] == '@H':
        factors = AIR_POLLUTANTS_H
        key_factors = AIR_POLLUTANTS_H
    else:
        factors = AIR_POLLUTANTS_7
        key_factors = AIR_POLLUTANTS
    tmp_data.columns = factors
    tmp_iaqi = pd.DataFrame(dtype=np.float, index = tmp_data.index, columns = factors)
    
    # calculate iaqi
    gaps = np.concatenate([[STANDARD_LIMITS[version].index[1:].values, STANDARD_LIMITS[version].index[:-1].values]]).T
    for [high, low] in gaps[::-1]:
        #print(high, low)
        _set_iaqi(tmp_iaqi, tmp_data, high, low, version)
        #print(tmp_iaqi.head())
    # 超上限数据
    tmp_iaqi[tmp_data > 500] = 501
    # 无效数据
    tmp_iaqi[tmp_data <= 0] = -1
    tmp_iaqi[tmp_data.isnull()] = -1
    if version[-2:] == '@H':
        # TODO: SO2-1H大于800后按SO2-24H计算
        index = tmp_iaqi.SO2 > 200
        # tmp_iaqi.loc[index, 'SO2'] = tmp_iaqi.loc[index, 'SO2_24H']
    else:
        # O3-8H大于800后按O3-1H计算
        index = tmp_iaqi.O3_8H > 300
        tmp_iaqi.loc[index, 'O3_8H'] = tmp_iaqi.loc[index, 'O3']
    # 修约
    tmp_iaqi = sci_round(tmp_iaqi, 0)
    
    # 无效数据
    index = tmp_iaqi <= 0
    index = index.sum(axis=1)>0
    # calculate AQI
    tmp_iaqi['AQI'] = tmp_iaqi[key_factors].max(axis=1)
    tmp_iaqi.loc[index, 'AQI']  = -1
    return tmp_iaqi.astype(np.int)

def _set_iaqi(tmp_iaqi, tmp_data, high, low, version='HJ663-2012'):
    if version[-2:] == '@H':
        factors = AIR_POLLUTANTS_H
    else:
        factors = AIR_POLLUTANTS_7
    low_end = _standards_v2m(STANDARD_LIMITS[version][factors].loc[low].values, len(tmp_iaqi), tmp_data)
    high_end = _standards_v2m(STANDARD_LIMITS[version][factors].loc[high].values, len(tmp_iaqi), tmp_data)
    #index = (tmp_data.as_matrix() <= high_end) & (tmp_data.as_matrix() > low_end)
    index = (tmp_data <= high_end) & (tmp_data > low_end)
    tmp = (tmp_data - low_end) / (high_end - low_end) * (high - low) + low
    tmp_iaqi[index] = tmp[index]
    return

def _standards_v2m(v, t, tmp_data, a=0):
    return pd.DataFrame(np.repeat(v.reshape(1, v.size), t, axis=a), index=tmp_data.index, columns=tmp_data.columns)