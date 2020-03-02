from flask import Flask
from .model_db import Song_Features, Base
import pandas as pd
from sqlalchemy import create_engine


def create_app():
    
    app = Flask(__name__)
    engine = create_engine('sqlite:///Spotify_Songs.db')
    Base.metadata.create_all(engine)
    file_name = 'https://raw.githubusercontent.com/aguilargallardo/DS-Unit-2-Applied-Modeling/master/data/SpotifyFeatures.csv'
    df = pd.read_csv(file_name)
    df.to_sql(con=engine, index_label='id', name=Song_Features.__tablename__, if_exists='replace')

    @app.route('/')
    def hello_world():
        return "Hello World!"

    @app.route('/data')
    def get_data():
        pass

    return app


    if __name__ == '__main__':
        app.run()