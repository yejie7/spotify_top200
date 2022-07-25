import os
import pandas as pd

col1 = ['uri',
        'rank',
        'artist_names',
        'artists_num',
        'artist_individual',
        'artist_id',
        'artist_genre',
        'artist_img',
        'collab',
        'track_name',
        'release_date',
        'album_num_tracks',
        'album_cover',
        'source',
        'peak_rank',
        'previous_rank',
        'weeks_on_chart',
        'streams',
        'week',
        'danceability',
        'energy',
        'key',
        'mode',
        'loudness',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'liveness',
        'valence',
        'tempo',
        'duration',
        'country',
        'region',
        'language',
        'pivot']

def cleanup(df):
    
    df = df[col1]
    df.to_csv('final.csv')
    
    return None

df = pd.read_csv('combined.csv')
cleanup(df)
