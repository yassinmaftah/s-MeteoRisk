import json
import pandas as pd

def json_to_dataframe(data_file) :
    with open(data_file,'r',encoding='utf-8') as f: 
        data_row = json.load(f)

    rows = []

    for r in data_row:
        # print(r.get("city"))
        city = r.get("city")
        daily_data = r.get("daily",{})

        time = daily_data.get("time",[])

        num_days = len(time)


        for i in range(num_days) :
            row = {
                'city' : city,
                'date' : time[i],
                'temperature_2m_max' : daily_data.get('temperature_2m_max',[None]*num_days)[i],
                'temperature_2m_min' : daily_data.get('temperature_2m_min',[None]*num_days)[i],
                'precipitation_probability_max' : daily_data.get('precipitation_probability_max',[None]*num_days)[i],
                'wind_speed_10m_max' : daily_data.get('wind_speed_10m_max',[None]*num_days)[i],
                'wind_gusts_10m_max' : daily_data.get('wind_gusts_10m_max',[None]*num_days)[i],
                'weather_code' : daily_data.get('weather_code',[None]*num_days)[i]
            }


            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv('../silver/df_silver.csv', index=False)

    return df








# df = json_to_dataframe('../bronze/raw_data.json')

# print(df.head(15))

