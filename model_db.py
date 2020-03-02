from numpy import genfromtxt
from time import time
from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=1, converters={0: lambda s: str(s)})
    return data.tolist()

Base = declarative_base()

class Song_Features(Base):
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

if __name__ == "__main__":
    t = time()

    #Create the database
    engine = create_engine('sqlite:///spotify_songs.db')
    Base.metadata.create_all(engine)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:
        file_name = "https://raw.githubusercontent.com/aguilargallardo/DS-Unit-2-Applied-Modeling/master/data/SpotifyFeatures.csv"
        data = Load_Data(file_name) 

        for i in data:
            record = Song_Features(**{
                'genre' : [0],
                'artist_name' : i[1],
                'track_name' : i[2],
                'track_id' : i[3],
                'popularity' : i[4],
                'acousticness' : i[5],
                'danceability' : i[6],
                'duration_ms' : i[7],
                'energy' : i[8],
                'instrumentalness' : i[9],
                'key' : i[10],
                'liveness' : i[11],
                'loudness' : i[12],
                'mode' : i[13],
                'speechiness' : i[14],
                'tempo' : i[15],
                'time_signature' : i[16],
                'valence' : i[17]
            })
            s.add(record) #Add all the records

        s.commit() #Attempt to commit all the records
    except:
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection