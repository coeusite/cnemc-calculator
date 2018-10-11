# Calculator@CNEMC
Unofficial calculator for air quality factors.

## Package Installation
To install with pip
``` bash
pip install --user git+https://github.com/coeusite/cnemc_calculator.git
```

## Dependency


## Usage
``` python3
# hourly AQI
# column_names = ['SO2', 'SO2_24H', 'NO2', 'PM10', 'CO', 'O3', 'PM_25'] for HJ663-2012
cnemc_calculator.calculate_hourly_aqi(data, column_names)

# daily AQI
# column_names = ['SO2', 'NO2', 'PM10', 'CO', 'O3', 'O3_8H', 'PM_25'] for HJ663-2012
cnemc_calculator.calculate_daily_aqi(data, column_names)
```
