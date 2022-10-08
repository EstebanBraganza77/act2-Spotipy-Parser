import spotipy
import json
import requests
import numpy as np
import pandas as pd
from act_02.auth import SpotOAuth


class PlayListParser:
    def __init__(self,id = SpotOAuth()._playlist):
        self.__oauth = SpotOAuth()._get_auth()
        self.__session = spotipy.Spotify(oauth_manager=self.__oauth)
        self._playlist_id = id
        self._playlist_tracks = []
        self._tracks_features = {
            'Track Name':[],
            'Tempo (BPM)':[],
            'Acousticness':[],
            'Danceability':[],
            'Energy':[],
            'Instrumentalness':[],
            'Liveness':[],
            'Loudness':[],
            'Valence':[]
        }
        self._get_cover()
        self._get_followers()
        self._get_tracks_features()
        self._get_mean_values()

    def _get_cover(self):
        img = self.__session.playlist_cover_image(playlist_id = self._playlist_id)[0]['url']
        response_img = requests.get(img)
        with open('./act_02/portadas/'+ 'playlist' +".jpg", "wb") as image:
            image.write(response_img.content)
            
    def _get_followers(self):
        playlist_ = self.__session.playlist(playlist_id = self._playlist_id)
        self._followers = {
            "Name": [playlist_['name']],
            'Followers': [playlist_['followers']['total']],
            'Description': [playlist_['description']]
            }
        pd.DataFrame(self._followers).to_csv('./act_02/ficheros/playlist.csv',index = False, sep=',')
    
    def _get_tracks_features(self):
        playlist_ = self.__session.playlist_tracks(playlist_id = self._playlist_id)
        for track in playlist_['items']:
            self._tracks_features['Track Name'].append(track['track']['name'])
            self._get_features(id = track['track']['id'])
        pd.DataFrame(self._tracks_features).to_csv('./act_02/ficheros/playlist_tracks_features.csv',index = False, sep=',')
        
    def _get_mean_values(self):
        track_features_mean = self._tracks_features.copy()
        del track_features_mean['Track Name']
        for feature in track_features_mean.keys():
            track_features_mean[feature] = round(sum(self._tracks_features[feature]) / len(self._tracks_features[feature]),2)
        pd.DataFrame(track_features_mean, index=[0]).to_csv('./act_02/ficheros/features_mean.csv',index = False, sep=',')
        
    def _get_features(self, id):
        track = self.__session.audio_features(tracks=id)
        self._tracks_features['Tempo (BPM)'].append(track[0]['tempo'])
        self._tracks_features['Acousticness'].append(track[0]['acousticness'])
        self._tracks_features['Danceability'].append(track[0]['danceability'])
        self._tracks_features['Energy'].append(track[0]['energy'])
        self._tracks_features['Instrumentalness'].append(track[0]['instrumentalness'])
        self._tracks_features['Liveness'].append(track[0]['liveness'])
        self._tracks_features['Loudness'].append(track[0]['loudness'])
        self._tracks_features['Valence'].append(track[0]['valence'])