import pandas as pd
from sqlalchemy.orm import sessionmaker

from create_db import engine, City, WeatherRisk
def get_temp_cat(temp):
    if temp < 15: 
        return 'Froid'
    if temp <= 25: 
        return 'Modéré'
    return 'Chaud'

def get_precip_cat(prob):
    if prob < 20: 
        return 'Faible'
    if prob <= 60: 
        return 'Moyenne'
    return 'Forte'

def get_wind_cat(wind):
    if wind < 20: 
        return 'Calme'
    if wind <= 50: 
        return 'Modéré'
    return 'Fort'
def insert_silver_data():

    Session = sessionmaker(bind=engine)

    session = Session()

    print("read data from silver")
    df = pd.read_csv('silver/df_silver.csv',parse_dates=['date'])

    print("start add categories")
    df['temp_category'] = df['temperature_2m_max'].apply(get_temp_cat)
    df['precip_category'] = df['precipitation_probability_max'].apply(get_precip_cat)
    df['wind_category'] = df['wind_gusts_10m_max'].apply(get_wind_cat)

    print('start with cities')

    cities_unique = df[['city','lat','lng']].drop_duplicates()
    cities_id = {} 
    for i, c in cities_unique.iterrows():
        check_city = session.query(City).filter_by(name=c['city']).first()
        if not check_city :
            new_city = City(name=c['city'],lat=c['lat'],lng=c['lng'])
            session.add(new_city)
            session.commit()
            cities_id[c['city']] = new_city.id
        else :
            cities_id[c['city']] = check_city.id

    print("start work on risk infos")

    new_data = []

    for i , row_city in df.iterrows():
        city_name = row_city['city']
        city_id = cities_id[city_name]

        date_d = row_city['date'].date()

        old_data = session.query(WeatherRisk).filter_by(city_id=city_id,date=date_d).first()

        if not old_data :
            new_day = WeatherRisk(
                city_id=city_id,
                date=date_d,
                temp_max=row_city['temperature_2m_max'],
                precip_max=row_city['precipitation_probability_max'],
                wind_gusts=row_city['wind_gusts_10m_max'],
                risk_total=row_city['risk_score_total'],
                temp_category=row_city['temp_category'],
                precip_category=row_city['precip_category'],
                wind_category=row_city['wind_category']
            )
            new_data.append(new_day)
        else :
            old_data.temp_max = row_city['temperature_2m_max']
            old_data.precip_max = row_city['precipitation_probability_max']
            old_data.wind_gusts = row_city['wind_gusts_10m_max']
            old_data.risk_total = row_city['risk_score_total']
            old_data.temp_category = row_city['temp_category']
            old_data.precip_category = row_city['precip_category']
            old_data.wind_category = row_city['wind_category']

    if new_data:
        session.bulk_save_objects(new_data)

    session.commit()
    session.close()
    print("insert new data done")




if __name__ == "__main__":
    insert_silver_data()

