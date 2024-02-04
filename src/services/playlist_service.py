from ..main import spotify_api
from typing import List, Dict


def get_all_playlist_tracks(playlist_id: str) -> List[Dict]:
    """
    Get all the tracks from a playlist
    """

    tracks = []
    results = spotify_api.playlist_items(playlist_id)

    while results:
        tracks += results['items']
        if results['next']:
            results = spotify_api.next(results)
        else:
            results = None

    return tracks


async def remove_all_tracks_from_playlist(playlist_id: str) -> bool:
    """
    Remove all the tracks from a playlist
    """

    try:
        tracks = get_all_playlist_tracks(playlist_id)

        track_ids = [track['track']['id'] for track in tracks]

        for i in range(0, len(track_ids), 100):
            track_ids_subset = track_ids[i:i+100]

            spotify_api.playlist_remove_all_occurrences_of_items(
                playlist_id, track_ids_subset)

        return True
    except Exception as e:
        print(f"An error occurred: {e}")

        return False


async def add_tracks_to_playlist(playlist_id: str, track_ids: List[str]) -> bool:
    """
    Add tracks to a playlist
    """

    try:
        for i in range(0, len(track_ids), 100):
            track_ids_subset = track_ids[i:i+100]

            spotify_api.playlist_add_items(playlist_id, track_ids_subset)

        return True
    except Exception as e:
        print(f"An error occurred: {e}")

        return False
