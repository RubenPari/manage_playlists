from sanic import Sanic
from sanic.response import json
from dotenv import load_dotenv
import os
import spotipy
from spotipy import SpotifyOAuth, Spotify
from models.hip_hop_enum import HipHopEnum
from services.playlist_service import add_tracks_to_playlist, remove_all_tracks_from_playlist
from services.track_service import get_all_user_tracks
from utils.artist_util import is_west_or_east_coast

app = Sanic("manage_playlists")

load_dotenv("./../.env")
scopes = os.getenv("SCOPES").split(" ")

spotify_api: Spotify


@app.get("/auth/login")
async def auth_login(request) -> json:
    global spotify_api

    spotify_api = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))

    return json({
        "message": "Successfully autenticate"
    })


@app.get("/auth/logout")
async def auth_logout(request) -> json:
    global spotify_api

    spotify_api = None

    return json({
        "message": "Successfully logout"
    })


@app.post("/playlist/create/hip-hop")
async def create_hip_hop_playlist(request) -> json:
    # get genre hip-hop query parameter
    genre = request.args.get("genre")

    # check if the genre is valid
    if genre and genre != "west-coast" and genre != "east-coast":
        return json({
            "message": "Invalid genre"
        }, status=400)

    # get hip-hop playlist
    playlist = spotify_api.playlist(os.getenv("HIP_HOP_PLAYLIST_ID"))

    # remove all old tracks from the playlist
    if not await remove_all_tracks_from_playlist(playlist['id']):
        return json({
            "message": "An error occurred while removing the old tracks"
        }, status=500)

    # get all tracks user
    tracks_users = await get_all_user_tracks()

    # filter the hip-hop tracks user
    hip_hop_tracks = list(
        filter(lambda track: "hip hop" in track['genres'], tracks_users))

    # filter the hip-hop tracks user based on the genre (if requested)
    if genre == "west-coast":
        for track in hip_hop_tracks:
            # get artist id
            artist_id = track['artists'][0]['id']

            if is_west_or_east_coast(artist_id) == HipHopEnum.EAST_COAST:
                hip_hop_tracks.remove(track)
    elif genre == "east-coast":
        for track in hip_hop_tracks:
            # get artist id
            artist_id = track['artists'][0]['id']

            if is_west_or_east_coast(artist_id) == HipHopEnum.WEST_COAST:
                hip_hop_tracks.remove(track)

    # add the hip-hop tracks to the playlist
    if not await add_tracks_to_playlist(playlist['id'], hip_hop_tracks):
        return json({
            "message": "An error occurred while adding the new tracks"
        }, status=500)

    return json({
        "message": "Successfully created the hip-hop playlist"
    })


@app.post("/playlist/create/pop")
async def create_pop_playlist(request) -> json:
    # get pop playlist
    playlist = spotify_api.playlist(os.getenv("POP_PLAYLIST_ID"))

    # remove all old tracks from the playlist
    if not await remove_all_tracks_from_playlist(playlist['id']):
        return json({
            "message": "An error occurred while removing the old tracks"
        }, status=500)

    # get all tracks user
    tracks_users = await get_all_user_tracks()

    # filter the pop tracks user
    pop_tracks = list(
        filter(lambda track: "pop" in track['genres'], tracks_users))

    # add the pop tracks to the playlist
    if not await add_tracks_to_playlist(playlist['id'], pop_tracks):
        return json({
            "message": "An error occurred while adding the new tracks"
        }, status=500)

    return json({
        "message": "Successfully created the pop playlist"
    })


@app.post("/playlist/create/edm")
async def create_edm_playlist(request) -> json:
    # get edm playlist
    playlist = spotify_api.playlist(os.getenv("EDM_PLAYLIST_ID"))

    # remove all old tracks from the playlist
    if not await remove_all_tracks_from_playlist(playlist['id']):
        return json({
            "message": "An error occurred while removing the old tracks"
        }, status=500)

    # get all tracks user
    tracks_users = await get_all_user_tracks()

    # filter the edm tracks user
    edm_tracks = list(
        filter(lambda track: "edm" in track['genres'], tracks_users))

    # add the edm tracks to the playlist
    if not await add_tracks_to_playlist(playlist['id'], edm_tracks):
        return json({
            "message": "An error occurred while adding the new tracks"
        }, status=500)

    return json({
        "message": "Successfully created the edm playlist"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT")))
