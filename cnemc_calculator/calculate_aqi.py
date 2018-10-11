import numpy as np
import pandas as pd

from .constants import *
from .functions import *

def calculate_daily_aqi(data, column_names, version='HJ663-2013'):
    ''' calculate_daily_aqi funcion
    
    data: a pandas dataframe
    column_names: names of factor columns insequence of ['SO2', 'NO2', 'PM10', 'CO', 'O3', 'O3_8H', 'PM_25']
    
    iAQI = 501 means it exceeds the upper limit
    
    '''
    tmp_data = data[column_names].convert_objects(convert_numeric=True)
    tmp_data.columns = AIR_POLLUTANTS_7
    tmp_iaqi = pd.DataFrame(dtype=np.float, index = tmp_data.index, columns = AIR_POLLUTANTS_7)
    
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
    # O3-8H大于800后按O3计算
    index = tmp_iaqi.O3_8H > 300
    tmp_iaqi.loc[index, 'O3_8H'] = tmp_iaqi.loc[index, 'O3']
    # 修约
    tmp_iaqi = sci_round(tmp_iaqi, 0)
    
    # calculate AQI
    tmp_iaqi['AQI'] = tmp_iaqi[AIR_POLLUTANTS].max(axis=1)
    return tmp_iaqi.astype(np.int)

def _set_iaqi(tmp_iaqi, tmp_data, high, low, version='HJ663-2013'):
    low_end = _standards_v2m(STANDARD_LIMITS[version][AIR_POLLUTANTS_7].loc[low].values, len(tmp_iaqi), tmp_data)
    high_end = _standards_v2m(STANDARD_LIMITS[version][AIR_POLLUTANTS_7].loc[high].values, len(tmp_iaqi), tmp_data)
    #index = (tmp_data.as_matrix() <= high_end) & (tmp_data.as_matrix() > low_end)
    index = (tmp_data <= high_end) & (tmp_data > low_end)
    tmp = (tmp_data - low_end) / (high_end - low_end) * (high - low) + low
    tmp_iaqi[index] = tmp[index]
    return

def _standards_v2m(v, t, tmp_data, a=0):
    return pd.DataFrame(np.repeat(v.reshape(1, v.size), t, axis=a), index=tmp_data.index, columns=tmp_data.columns)