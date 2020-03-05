from flask import Flask, jsonify
import sqlite3
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import numpy as np
from sklearn import preprocessing  # for category encoder
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from typing import List, Tuple

DB = SQLAlchemy()
#df = pd.read_csv(
    #'https://raw.githubusercontent.com/msnyd/spotify_song_suggestor/master/most_popular_spotify_songs.csv')


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

    #DB = SQLAlchemy()

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://Spotify_Songs.db"
    
    engine = create_engine('sqlite:///Spotify_Songs.db')
    Songs.metadata.create_all(engine)
    file_name = 'https://raw.githubusercontent.com/msnyd/spotify_song_suggestor/master/app/most_popular_spotify_songs.csv'
    df = pd.read_csv(file_name)
    db = df.to_sql(con=engine, index_label='id',
                   name=Songs.__tablename__, if_exists='replace')


    def pre_process(df):
        time_sig_encoding = {'0/4': 0, '1/4': 1,
                             '3/4': 3, '4/4': 4,
                             '5/4': 5}
        key_encoding = {'A': 0, 'A#': 1, 'B': 2,
                        'C': 3,  'C#': 4,  'D': 5,
                        'D#': 6, 'E': 7, 'F': 8,
                        'F#': 9, 'G': 10, 'G#': 11}
        mode_encoding = {'Major': 0, 'Minor': 1}
        df['key'] = df['key'].map(key_encoding)
        df['time_signature'] = df['time_signature'].map(time_sig_encoding)
        df['mode'] = df['mode'].map(mode_encoding)
        # helper function to one hot encode genre

        def encode_and_bind(original_dataframe, feature_to_encode):
            dummies = pd.get_dummies(original_dataframe[[feature_to_encode]])
            res = pd.concat([original_dataframe, dummies], axis=1)
            return(res)
        df = encode_and_bind(df, 'genre')
        return df

    """
    This will run the nearest neighbors model when we instantiate the app.
    """
    processed_df = pre_process(df)

    neigh = NearestNeighbors(n_neighbors=11)
    features = list(processed_df.columns[4:])
    X = processed_df[features].values
    neigh.fit(X)

    def closest_ten(df: pd.DataFrame, X_array: np.ndarray, song_id: int) -> List[Tuple]:
        song = df.iloc[song_id]
        X_song = X[song_id]
        _, neighbors = neigh.kneighbors(np.array([X_song]))
        return neighbors[0][1:]

    # @app.route('/populate')
    # def populate():
    #     engine = create_engine('sqlite:///Spotify_Songs.db')
    #     Songs.metadata.create_all(engine)
    #     file_name = 'https://raw.githubusercontent.com/msnyd/spotify_song_suggestor/master/most_popular_spotify_songs.csv'
    #     df = pd.read_csv(file_name)
    #     db = df.to_sql(con=engine, index_label='id',
    #             name=Songs.__tablename__, if_exists='replace')
    #     return "Database has been made!"

    @app.route('/')
    def hello_world():

        return "Welcome to our Spotify API!"

    # #TODO make a route that takes in json data and converts it to match the database?
    # @app.route('/user/data')
    # def user_data():
    #     pass

    # #Model returns a list of songs and we return the top 10
    # @app.route('/songs', methods=['GET'])
    # def get_songs():
    #     conn = sqlite3.connect('sqlite://Spotify_Songs.db')
    #     conn.row_factory = dict_factory
    #     curs = conn.cursor()
    #     all_songs = curs.execute(
    #         'SELECT track_name, artist_name, genre FROM songs LIMIT 10;').fetchall()

    #     return jsonify(all_songs)

    @app.route('/track/<track_id>', methods=['GET'])  # /<track_id>
    def track(track_id):
        track_id = int(track_id)
        conn = sqlite3.connect('Spotify_Songs.db')
        conn.row_factory = dict_factory
        curs = conn.cursor()
        #idx = curs.execute(f'SELECT id from songs where track_id=={track_id};').fetchall()
        songlist = []
        song_recs = closest_ten(df, X, track_id)
        for idx in song_recs:
            song = curs.execute(
                f'SELECT DISTINCT id, track_name, artist_name, genre, track_id FROM Songs WHERE id=={idx};').fetchone()

            songlist.append(song)
        #songlist = tuple(songlist)
        #songlist = list(dict.fromkeys(songlist)) # removes duplicates

        return jsonify(songlist)

    return app