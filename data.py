import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import pandas as pd
import random
import time
import sys

cid = '65ec98f08d5d4dc693050ec93a1d02bb'
secret = '3a8cb12b3b7248f08cdf4ed2bf4a6785'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

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

genres_list = []


def get_audio_features(df):
    
    tids = list(df['uri'])
    df = df
    index = 0
    features = []
    while index < len(tids):
        if index + 100 < len(tids):
            print(index)
            features0 = sp.audio_features(tids[index:index+100])
        else:
            features0 = sp.audio_features(tids[index:])
        features.extend(features0)
        index += 100

    print('audio queries done')
    features = [{'danceability': None, 'energy': None, 'key': None, 'loudness': None, 'mode': None, 'speechiness': None, 'acousticness': None, 'instrumentalness': None, 'liveness': None, 'valence': None, 'tempo': None, 'type': 'audio_features', 'id': '', 'uri': '', 'track_href': '', 'analysis_url': '', 'duration_ms': None, 'time_signature': None} if v is None else v for v in features]
    #print(features)
    
    features_df = pd.DataFrame(features)
    df['danceability'] = features_df['danceability']
    df['energy'] = features_df['energy']
    df['key'] = features_df['key']
    df['mode'] = features_df['mode']
    df['loudness'] = features_df['loudness']
    df['speechiness'] = features_df['speechiness']
    df['acousticness'] = features_df['acousticness']
    df['instrumentalness'] = features_df['instrumentalness']
    df['liveness'] = features_df['liveness']
    df['valence'] = features_df['valence']
    df['tempo'] = features_df['tempo']
    df['duration'] = features_df['duration_ms']
    
    return df

def get_tracks(tids):
    
    index = 0
    features = []
    
    while index < len(tids):
        if index + 50 < len(tids):
            features0 = sp.tracks(tids[index:index+50])
        else:
            features0 = sp.tracks(tids[index:])
        features.extend(features0['tracks'])      
        index += 50
        print(index)

    print('track queries done')

    return features

def get_track_features_pivot(df, features):

    df = df
    tids = list(df['uri'])
    
    for i, feature in enumerate(features):
        tid = tids[i]
        if feature != 'null':
            print(i)
            artist_list = []
            artist_names = []
            df.loc[i, 'release_date'] = feature['album']['release_date']
            df.loc[i, 'album_num_tracks'] = feature['album']['total_tracks']
            if len(feature['album']['images']) > 0:
                df.loc[i, 'album_cover'] = feature['album']['images'][0]['url']

            for artist in feature['artists']:
                artist_list.append(artist['uri'])
                artist_names.append(artist['name'])
                
            if len(artist_list) > 1:
                for x in range(0, len(artist_list)):
                    new_row = df.iloc[[i]]
                    new_row['artist_individual'] = artist_names[x]
                    new_row['artist_id'] = artist_list[x]
                    new_row['collab'] = 1
                    if x != 0:
                        new_row['pivot'] = 1
                    df = pd.concat([df, new_row])
            else:
                df.loc[i, 'artist_id'] = artist_list[0]
                df.loc[i, 'artist_individual'] = artist_names[0]
            df.loc[i, 'artists_num'] = len(artist_list)
            
    return df

def delete_collab(df):

    df = df
    index = 0  
    for i in df.index:
        if i == len(df.index)-1:
            break
        if df.loc[index, ['artist_individual']].isnull().values.any():
            df = df.drop(df.index[index])
            index -= 1  
        index += 1
        df = df.reset_index(drop=True)

        print(i)
        
    return df

def get_artists(artist_ids):
    
    artist_ids = artist_ids
    features = []
    index = 0
    
    while index < len(artist_ids):
        if index + 50 < len(artist_ids):
            features0 = sp.artists(artist_ids[index:index+50])
            #print(features0)
        else:
            features0 = sp.artists(artist_ids[index:])
        features.extend(features0['artists'])      
        index += 50
        print(index)

    print('artist queries done')
    
    return features

def get_artist_features(df, features):

    df = df
    df['artist_genre'] = 0
    artist_ids = list(df['artist_id'])
    
    for i, feature in enumerate(features):
        artist_id = artist_ids[i]
        if feature: 
            genre = 0 
            #print(feature)
            genres = random.sample(feature['genres'], len(feature['genres']))
            index = 0 
            while index < len(genres):
                if genres[index] in genres_list:
                    genre = genres[index]
                    df.loc[i, 'artist_genre'] = genre
                    #print(genre, 'genre')
                    break
                else:
                    index += 1 
                    genre = genres[0]
                    genres_list.append(genre)

            if df.loc[i, 'artist_genre'] == 0 and len(genres) != 0:
                df.loc[i, 'artist_genre'] = genre
                
            if len(feature['images']) > 0:
                df.loc[i, 'artist_img'] = feature['images'][0]['url']
        #print(df.loc[[i]])
        print(i)
            
    return df

country_list = ['morocco']

for country in country_list:

    cname = country
    df = pd.DataFrame(columns=col1)
    df_init = pd.read_csv('regionals_concat/weekly_' + cname + '.csv')
    df['uri'] = df_init['uri']
    df['rank'] = df_init['rank']
    df['artist_names'] = df_init['artist_names']
    df['artist_genre'] = 0
    df['track_name'] = df_init['track_name']
    df['source'] = df_init['source']
    df['peak_rank'] = df_init['peak_rank']
    df['previous_rank'] = df_init['previous_rank']
    df['weeks_on_chart'] = df_init['weeks_on_chart']
    df['streams'] = df_init['streams']
    df['week'] = df_init['date']
    df['country'] = df_init['country']
    df['region'] = df_init['continent']
    df['language'] = df_init['language']
    df['collab'] = 0
    df['pivot'] = 0

    pd.options.mode.chained_assignment = None  # default='warn'
    get_audio_features(df).to_csv(cname + '_audio.csv')
    df_audio = pd.read_csv(cname + '_audio.csv')
    features = get_tracks(list(df['uri']))
    get_track_features_pivot(df_audio, features).to_csv(cname + '_features.csv')
    df_features = pd.read_csv(cname + '_features.csv')
    delete_collab(df_features).to_csv(cname +'_cleaned.csv')
    df_cleaned = pd.read_csv(cname + '_cleaned.csv')
    artist_ids = list(df_cleaned['artist_id'])
    jsonString = json.dumps(get_artists(artist_ids))
    jsonFile = open(cname + ".json", "w")
    jsonFile.write(jsonString)
    f = open(cname + '.json')  
    artist_features = json.load(f)  
    get_artist_features(df_cleaned, artist_features).to_csv('finals/' + cname + '_final.csv')
