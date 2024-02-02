from ..server import spotify_api

def get_first_artist_genre(artist_id):
    artist_info = spotify_api.artist(artist_id)
    
    genres = artist_info.get('genres', [])
    
    if genres:
        return genres[0]
    else:
        return "Nessun genere trovato per questo artista."