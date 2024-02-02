from sanic import Sanic
from sanic.response import json
from dotenv import load_dotenv
import os
import spotipy
from spotipy import SpotifyOAuth

app = Sanic("manage_playlists")

load_dotenv()
scopes = os.getenv("SCOPES").split()

spotify_api = None

@app.get("/auth/login")
async def auth_login(request):
    spotify_api = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))

    return json({
        "message": "Successfully autenticate"
    })

@app.get("/auth/logout")
async def auth_logout(request):
    spotify_api = None

    return json({
        "message": "Successfully logout"
    })

