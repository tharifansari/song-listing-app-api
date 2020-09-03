import subprocess
from components.hasura_controller import HasuraClient
from components import ratings
import hashlib
import json
import uuid
import sys
from heapq import nlargest 
import numpy as np

sys.path.append(".")

graphQL_client = HasuraClient().graphql_client

# name dob bio

def get_all_artist():
    query = """
    {
        artist{
            id 
            name
            dob
            bio
        }
    }
    """
    result = json.loads(graphQL_client.execute(query))
    if "errors" not in result:
        return True, result['data']['artist']
    return False, "query error"

def add_artist(data):
    # YYYY-MM-DD
    if "name" not in data or "dob" not in data or "bio" not in data:
        return False, "name, dob or date is not present in the request body"
    artist_id = str(uuid.uuid4())
    query="""
        mutation MyMutation {
            insert_artist(objects: {id:"$id$",name:"$name$",dob:"$dob$",bio:"$bio$"}) {
                affected_rows
            }
        }
    """.replace("$id$",artist_id).replace("$name$",data['name'])\
        .replace("$dob$",str(data['dob'])).replace("$bio$",data['bio'])
    result = json.loads(graphQL_client.execute(query))
    if "errors" not in result:
        return True, "Successfully added an artist"
    return False, result['errors'][0]["message"]


def get_song_artist(artist_id):
    query=""" 
    {
        song_artist(where: {artist_id: {_eq: "$a_id$"}}) {
            song_id
        }
    }
    """.replace("$a_id$",artist_id)
    result = json.loads(graphQL_client.execute(query))['data']['song_artist']
    songs_list = []
    for song in result:
        songs_list.append(song['song_id'])
    return songs_list

def get_rating_for_songs(song_id):
    query="""
        {
            rating(where:{song_id:{_eq:"s_id"}}){
                rating
            }
        }
    """.replace("$s_id$",json.dumps(song_id))
    result = json.loads(graphQL_client.execute(query))['data']['rating']
    rating_list = []
    for ratng in result:
        rating_list.append(ratng['rating'])
    return rating_list


def top_artist(songs, top):
    # get all artist, get songs sung by each artist, find rating for each song
    
    status, all_artist = get_all_artist()

    
    if status == True:
        rating_dict = {}
        for each_artst in all_artist:
            songs_ls = get_song_artist(each_artst['id'])
            rating_dict[each_artst['id']] = get_rating_for_songs(songs_ls)
        
        rating_average = {}
        for artst in rating_dict:
            rating_average[artst] = np.mean(rating_dict[artst])
        print(rating_average)
        top_artist_keys = nlargest(top, rating_average, key = rating_average.get) 
        return True, top_artist_keys
    return False, all_artist