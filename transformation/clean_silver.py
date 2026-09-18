import pandas as pd
import numpy as np
# from transformation.clean_silver import json_to_dataframe
# from json_to_df import json_to_dataframe
from transformation.json_to_df import json_to_dataframe

def clean_data(df):
    df.fillna(0, inplace=True)
    
    df['date'] = pd.to_datetime(df['date'])

    expected_dates = df['date'].shift(1).apply(fix_mission_day)
    df['date'] = df['date'].fillna(expected_dates)

    weather_cols = [
        'temperature_2m_max', 'temperature_2m_min', 
        'precipitation_probability_max', 'wind_speed_10m_max', 
        'wind_gusts_10m_max', 'weather_code'
    ]
    df[weather_cols] = df[weather_cols].ffill()

    df.drop_duplicates(inplace=True)
    cities_df = pd.read_csv('bronze/ma.csv')
    df = pd.merge(df, cities_df[['city', 'lat', 'lng']], on='city', how='left')
    df = calculate_risk_features(df)
    df.to_csv('silver/df_silver.csv', index=False)
    return df

def fix_mission_day(date):
    return date + pd.Timedelta(days=1)

def calculate_risk_features(df):
    wind_conditions = [
        df['wind_gusts_10m_max'] > 85,
        df['wind_gusts_10m_max'] > 60,
        df['wind_gusts_10m_max'] > 40
    ]
    wind_scores = [50, 30, 15]
    df['risk_wind'] = np.select(wind_conditions, wind_scores, default=0)
    df['risk_rain'] = df['precipitation_probability_max'] * 0.3

    temp_condition = (df['temperature_2m_max'] > 40) | (df['temperature_2m_min'] < 2)
    df['risk_temp'] = np.where(temp_condition, 20, 0)

    df['risk_score_total'] = df['risk_wind'] + df['risk_rain'] + df['risk_temp']

    df['risk_score_total'] = np.where(df['risk_score_total'] > 100, 100, df['risk_score_total'])
    all_risk_cols = ['risk_wind', 'risk_rain', 'risk_temp', 'risk_score_total']
    df[all_risk_cols] = df[all_risk_cols].round(2)
    return df

# df = json_to_dataframe('../bronze/data01.json')
# cleaned_df = clean_data(df)

def x2():
    df = json_to_dataframe('bronze/data01.json')
    clean_data(df)


# print(cleaned_df.info())
# print("\nMissing values per column:")
# print(cleaned_df.isnull().sum())
# print(cleaned_df.info())