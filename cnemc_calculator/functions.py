import numpy as np
import pandas as pd


def sci_round(df, digi=0):
    ''' sci_round function
        四舍六入五成双修约函数近似算法
    '''
    return np.round(np.round(df, 15), digi)