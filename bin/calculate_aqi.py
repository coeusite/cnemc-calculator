import pandas as pd
import numpy as np
import cnemc_calculator

from importlib import reload

# calculate_daily_aqi
cnemc_calculator = reload(cnemc-calculator)

data = pd.read_excel('data/审核后点位日均值.xlsx', header=0, index_col=[3,4], na_values=[-1,-99])
cnemc_calculator.calculate_daily_aqi(data, columns)