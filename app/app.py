from flask import Flask, jsonify
#from sqlalchemy import create_engine
import sqlite3
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

DB = SQLAlchemy()


class Songs(DB.Model):
    __tablename__ = "Songs"
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    id = DB.Column(DB.BigInteger, primary_key=True)
    genre = DB.Column(DB.String(50))
    artist_name = DB.Column(DB.String(50))
    track_name = DB.Column(DB.String(100))
    track_id = DB.Column(DB.String(50))
    popularity = DB.Column(DB.Integer)
    acousticness = DB.Column(DB.Float)
    danceability = DB.Column(DB.Float)
    duration_ms = DB.Column(DB.Integer)
    energy = DB.Column(DB.Float)
    instrumentalness = DB.Column(DB.Float)
    key = DB.Column(DB.Integer)
    liveness = DB.Column(DB.Float)
    loudness = DB.Column(DB.Float)
    mode = DB.Column(DB.Integer)
    speechiness = DB.Column(DB.Float)
    tempo = DB.Column(DB.Float)
    time_signature = DB.Column(DB.Integer)
    valence = DB.Column(DB.Float)

    def __repr__(self):
        return '<Song {}>'.format(self.track_name)



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_app():
    app = Flask(__name__)


    @app.route('/populate')
    def populate():
        engine = create_engine('sqlite:///Spotify_Songs.db')
        Songs.metadata.create_all(engine)
        file_name = 'https://raw.githubusercontent.com/aguilargallardo/DS-Unit-2-Applied-Modeling/master/data/SpotifyFeatures.csv'
        df = pd.read_csv(file_name)
        DB = df.to_sql(con=engine, index_label='id',
                name=Songs.__tablename__, if_exists='replace')
        return "Database has been made!"

    @app.route('/')
    def hello_world():
        return "Hello World!"

    #TODO make a route that takes in json data and converts it to match the database?
    @app.route('/user/data')
    def user_data():
        pass

    #Model returns a list of songs and we return the top 10
    @app.route('/songs', methods=['GET']) #methods=['GET'])
    def get_songs():
        conn = sqlite3.connect('Spotify_Songs.db')
        conn.row_factory = dict_factory
        curs = conn.cursor()
        all_songs = curs.execute('SELECT track_name, artist_name, genre FROM songs LIMIT 10;').fetchall()

        return jsonify(all_songs)

    return app