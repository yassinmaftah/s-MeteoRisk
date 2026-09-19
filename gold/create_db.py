import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / '.env')

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 's_meteorisk_db')

DATABASE_URL = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class City(Base) :
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    weather_logs = relationship("WeatherRisk", back_populates="city")

class WeatherRisk(Base):
    __tablename__ = 'weather_risks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    date = Column(Date, nullable=False)
    temp_max = Column(Float)
    precip_max = Column(Float)
    wind_gusts = Column(Float)
    risk_total = Column(Float)

    temp_category = Column(String(50))
    precip_category = Column(String(50))
    wind_category = Column(String(50))
    city = relationship("City", back_populates="weather_logs")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables 'cities' and 'weather_risks' created successfully.")