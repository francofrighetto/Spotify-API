import spotipy
#from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv("../.env"))

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
username = os.getenv('USERNAME')

"""
scope='user-modify-playback-state'   ->  para reproducir musica
scope='user-read-playback-state'     -> para obtener dispositivos (tiene que estar abierto spotify en el dispositivo sino no devuelve nada)
scope='playlist-modify-public'       -> para obtener datos de playlist
"""
token = util.prompt_for_user_token(
    username=username,
    scope='user-modify-playback-state',
    client_id=client_id, 
    client_secret=client_secret, 
    redirect_uri=os.getenv('REDIRECT_URL')
)

sp = spotipy.Spotify(auth=token)
playlist_link = os.getenv('URL_FUSION')
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
canciones=[]
for track in sp.playlist_tracks(playlist_URI)["items"]:
    if track["added_by"]["id"] == os.getenv('ID_FUSION'):
        canciones.append(track["track"]["uri"])

sp.start_playback(device_id=os.getenv('DEVICE_ID'), uris=canciones)

# para poner toda la info del tema pongo print(track)