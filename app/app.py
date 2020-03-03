from flask import Flask, jsonify
from .model_db import Songs
from sqlalchemy import create_engine
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_app():
    app = Flask(__name__)

    # engine = create_engine('sqlite:///Spotify_Songs.db')
    # Songs.metadata.create_all(engine)
    # file_name = 'data\SpotifyFeatures.csv'
    # df = pd.read_csv(file_name)
    # DB = df.to_sql(con=engine, index_label='id',
    #            name=Songs.__tablename__, if_exists='replace')

    @app.route('/')
    def hello_world():
        return "Hello World!"

    #TODO make a route that takes in json data and converts it to match the database?
    @app.route('/user/data')
    def user_data():
        pass

    #Model returns a list of songs and we return the top 10
    @app.route('/get/songs') #methods=['GET'])
    def get_songs():
        conn = sqlite3.connect('Spotify_Songs.db')
        conn.row_factory = dict_factory
        curs = conn.cursor()
        all_songs = curs.execute('SELECT track_name, artist_name, genre FROM Spotify_Songs LIMIT 10;').fetchall()
        return jsonify(all_songs)

    return app
