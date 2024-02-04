from ..main import spotify_api


async def get_all_user_tracks() -> list:
    """
    Get all the tracks saved by the user
    """

    saved_tracks = []

    results = spotify_api.current_user_saved_tracks()

    while results:
        saved_tracks += results['items']
        if results['next']:
            results = spotify_api.next(results)
        else:
            results = None

    return saved_tracks
