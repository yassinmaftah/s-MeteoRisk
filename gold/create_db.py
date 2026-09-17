from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

DB_USER = "postgres"
DB_PASS = "ysn.mfth"
DB_HOST = "meteorisk_db"
DB_NAME = "s_meteorisk_db"

engine = create_engine(f"postgresql+pg8000://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")

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
    city = relationship("City", back_populates="weather_logs")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables 'cities' and 'weather_risks' created successfully.")