from spotipy.oauth2 import SpotifyOAuth

class SpotOAuth:
    __client_id = '7902a18797f24ac19208b979cf71d630'
    __client_secret = 'c236c74f861d4cf7b7fc299cdbfb6d0a'
    __redirect_url = 'http://localhost:9000'
    _playlist ='37i9dQZF1DWWGFQLoP9qlv'
    __scope = ['user-top-read','playlist-read-private',]
    
    def _get_auth(self):
        return SpotifyOAuth(client_id = SpotOAuth.__client_id, 
                                               client_secret = SpotOAuth.__client_secret,
                                               redirect_uri=SpotOAuth.__redirect_url ,
                                               scope=SpotOAuth.__scope)