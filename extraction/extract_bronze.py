import pandas as pd
import requests
import time
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_cites(file_path) :
    df = pd.read_csv(file_path,encoding='utf-8')
    return df[['city','lat','lng']]

# print(load_cites('../bronze/ma.csv'))


def fetch_data_with_API(cities) :
    row_data_list = []
    base_url_API = "https://api.open-meteo.com/v1/forecast"

    for i , row in cities.iterrows(): 
        city = row['city']

        params = {
            "latitude": row['lat'],
            "longitude": row['lng'],
            "daily": [
                "temperature_2m_max", 
                "temperature_2m_min", 
                "precipitation_sum", 
                "precipitation_probability_max", 
                "wind_speed_10m_max", 
                "wind_gusts_10m_max", 
                "weather_code"
            ],
            "timezone": "auto"
        }

        print(f"start with : {city}\n")
        try :
            response = requests.get(base_url_API, params=params, timeout=10)
            response.raise_for_status() 
            weather_data = response.json()
            weather_data['city'] = city
            row_data_list.append(weather_data)

        except requests.exceptions.RequestException as e :
            print(f"city : {city}, error : {e}")

        time.sleep(0.1)
    return row_data_list

# C:\Users\yassi\OneDrive\Desktop\s-MeteoRisk\bronze\ma.csv

def save_to_bronze(data,file_path) :
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Done")


def x():
    cities = load_cites(PROJECT_ROOT / 'bronze' / 'ma.csv')

    new_data = fetch_data_with_API(cities)

    save_to_bronze(new_data, PROJECT_ROOT / 'bronze' / 'data01.json')
