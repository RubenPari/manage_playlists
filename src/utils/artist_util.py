from ..main import spotify_api
from openai import OpenAI

from ..models.hip_hop_enum import HipHopEnum


def get_first_artist_genre(artist_id) -> str:
    artist_info = spotify_api.artist(artist_id)

    genres = artist_info.get('genres', [])

    if genres:
        return genres[0]
    else:
        return "Nessun genere trovato per questo artista."


async def is_west_or_east_coast(artist_id) -> HipHopEnum:
    artist_info = spotify_api.artist(artist_id)

    # get the artist's name
    artist_name = artist_info.get('name', '')

    client = OpenAI()

    # ask chatbot if the artist is from the east or west coast
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Is " + artist_name +
                                        " from the west or east coast? (Respond with 'East Coast' or 'West Coast')"}
        ]
    )

    response = completion['choices'][0]['message']['content']

    # return the enum value based on the response
    if response.lower() == "east coast":
        return HipHopEnum.EAST_COAST
    elif response.lower() == "west coast":
        return HipHopEnum.WEST_COAST
