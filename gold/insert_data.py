import pandas as pd
from sqlalchemy.orm import sessionmaker

from create_db import engine, City, WeatherRisk

def insert_silver_data():

    Session = sessionmaker(bind=engine)

    session = Session()

    print("read data from silver")
    df = pd.read_csv('silver/df_silver.csv',parse_dates=['date'])
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
                risk_total=row_city['risk_score_total']
            )
            new_data.append(new_day)
        else :
            old_data.temp_max = row_city['temperature_2m_max']
            old_data.precip_max = row_city['precipitation_probability_max']
            old_data.wind_gusts = row_city['wind_gusts_10m_max']
            old_data.risk_total = row_city['risk_score_total']

    if new_data:
        session.bulk_save_objects(new_data)

    session.commit()
    session.close()
    print("insert new data done")




if __name__ == "__main__":
    insert_silver_data()

