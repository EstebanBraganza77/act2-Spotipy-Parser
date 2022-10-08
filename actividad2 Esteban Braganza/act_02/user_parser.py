import spotipy
import json
import requests
import numpy as np
import pandas as pd
from act_02.auth import SpotOAuth

class SpotifyParser:
    def __init__(self):
        self.__oauth = SpotOAuth()._get_auth()
        self.__session = spotipy.Spotify(oauth_manager=self.__oauth)
        self._top_artists_names = {'top_artists':[]}
        self._top_genres = {'top_genres':[]}
        self._top_tracks = {'name':[], 'artist':[], 'album':[], 'release_date':[],'tracks':[]}
        self._album_data = {'name':[],'image_url':[],'album_id':[]}
        self._track_id = []
        self._albums = []
        self._get_data()
    
    def _parse_top_artists_data(self,limit = 10):
        raw_results = self.__session.current_user_top_artists(limit=limit)
        if raw_results['items']:
            for item in raw_results['items']:
                self._top_artists_names['top_artists'].append(item['name'])
                self._top_genres['top_genres'] += item['genres']

    def _parse_top_tracks_data(self,limit = 20):
        raw_results = self.__session.current_user_top_tracks(limit=limit)
        if raw_results['items']:
            for item in raw_results['items']:
                self._top_tracks['name'].append(item['name'])
                self._top_tracks['artist'].append(item['album']['artists'][0]['name'])
                self._track_id.append(item['id'])
        self._get_album_data()
     
    def _get_album_data(self):
        # Tracks album data
        for id in self._track_id:
            tracks = self.__session.track(track_id = id)
            self._top_tracks['album'].append(tracks['album']['name']) 
            self._top_tracks['release_date'].append(tracks['album']['release_date']) 
            self._album_data['image_url'].append(tracks['album']['images'][0]['url'])
            self._album_data['name'].append(tracks['album']['name']) 
            self._album_data['album_id'].append(tracks['album']['id'])
        self._save_images()
        self._get_album_tracks()
            
    def _get_album_tracks(self):
        # Albums tracks
        for id in self._album_data['album_id']:
            album_ = self.__session.album_tracks(album_id = id)
            self._top_tracks['tracks'].append([track['name'] for track in album_['items']])
            
    def _save_images(self):
        for img in self._album_data['image_url']:
            index = self._album_data['image_url'].index(img)
            name = self._album_data['name'][index]
            response_img = requests.get(img)
            with open('./act_02/portadas/'+ name +".jpg", "wb") as image:
                image.write(response_img.content)
        
    def _write_csv_files(self):
        tracks_df = pd.DataFrame(self._top_tracks)
        tracks_df.to_csv('./act_02/ficheros/user_top_tracks.csv',index = False, sep=',')
        artist_df = pd.DataFrame(self._top_artists_names)
        artist_df.to_csv('./act_02/ficheros/user_top_artists.csv',index = False, sep=',')
        genres_df = pd.DataFrame(self._top_genres)
        genres_df.drop_duplicates(inplace=True)
        genres_df.to_csv('./act_02/ficheros/user_top_genres.csv',index = False, sep=',')
    
    def _get_data(self):
        self._parse_top_artists_data()
        self._parse_top_tracks_data()
        self._write_csv_files()

            

        
        
    

