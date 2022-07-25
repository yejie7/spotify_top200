import os
import pandas as pd

col_weekly = ['rank', 'uri', 'artist_names','track_name', 'source',
              'peak_rank', 'previous_rank', 'weeks_on_chart', 'streams', 'date',
              'country', 'continent', 'language']

directory = 'directory_name'
country = 'country_name'
continent = 'region_name'
language = 'language_name'

#combine all csv files in the directory to one
def weekly_concat(directory):
    
    directory = directory
    df = pd.DataFrame(columns=col_weekly)

    for filename in os.listdir(directory):
        
        f = os.path.join(directory, filename)
    
        # checking if it is a file
        if os.path.isfile(f):
            #print(f)
            df_week = pd.read_csv(f)
            date = f[-14:-4]      
            df_week['date'] = date
            df_week['country'] = country
            df_week['continent'] = continent
            df_week['language'] = language
            df = pd.concat([df,df_week])

    df.to_csv('file_name')

    return None

weekly_concat(directory)
