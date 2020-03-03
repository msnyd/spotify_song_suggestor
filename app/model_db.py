from numpy import genfromtxt
from time import time
from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import pandas as pd


Base = declarative_base()

class Songs(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'Spotify_Songs'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer, primary_key=True, nullable=False) 
    genre = Column(String(50))
    artist_name = Column(String(50))
    track_name = Column(String(100))
    track_id = Column(String(50))
    popularity = Column(Integer)
    acousticness = Column(Float)
    danceability = Column(Float)
    duration_ms = Column(Integer)
    energy = Column(Float)
    instrumentalness = Column(Float)
    key = Column(Integer)
    liveness = Column(Float)
    loudness = Column(Float)
    mode = Column(Integer)
    speechiness = Column(Float)
    tempo = Column(Float)
    time_signature = Column(Integer)
    valence = Column(Float)
# engine = create_engine('sqlite:///Spotify_Songs.db')
# Base.metadata.create_all(engine)
# file_name = 'https://raw.githubusercontent.com/aguilargallardo/DS-Unit-2-Applied-Modeling/master/data/SpotifyFeatures.csv'
# df = pd.read_csv(file_name)
# df.to_sql(con=engine, index_label='id', name=Song_Features.__tablename__, if_exists='replace')