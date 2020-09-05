import subprocess
from components.hasura_controller import HasuraClient
from components import ratings
import hashlib
import json
import uuid
import sys
import numpy as np
from heapq import nlargest 

sys.path.append(".")

graphQL_client = HasuraClient().graphql_client


def get_all_songs():
    query = """
    {
        songs{
            id 
            name
            date
        }
    }
    """
    result = json.loads(graphQL_client.execute(query))
    if "errors" not in result:
        return True, result['data']['songs']
    return False, "query error"

def top_songs(songs, top):
    status, all_ratings = ratings.get_all_ratings()
    if status == True:
        rating_dict = {}
        for each_rating in all_ratings:
            if each_rating['song_id'] not in rating_dict:
                rating_dict[each_rating['song_id']] = []
                rating_dict[each_rating['song_id']].append(each_rating['rating'])
            else:
                rating_dict[each_rating['song_id']].append(each_rating['rating'])
        rating_average = {}
        for song in rating_dict:
            rating_average[song] = np.mean(rating_dict[song])
        top_song_keys = nlargest(top, rating_average, key = rating_average.get) 
        return True, top_song_keys
    return False, all_ratings


def song_artist_query():
    return '''
    mutation insert_song_artist($rows: [song_artist_insert_input!]!) {
        insert_song_artist(objects: $rows, on_conflict: {constraint: song_artist_pkey, update_columns: [song_id, artist_id]}) {
            affected_rows
        }
    }'''
    


def artist_query(artist):
    return """
        {
            artist(where: {name: {_eq: "$name$"}}){
                id
            }
        }
    """.replace("$name$",artist)

def add_song(data):
    # YYYY-MM-DD
    if "name" not in data or "date" not in data or "artist" not in data:
        return False, "name, date or artist is not present in the request body"
    song_id = str(uuid.uuid4())
    query="""
        mutation MyMutation {
            insert_songs(objects: {id:"$id$",name:"$name$",date:"$date$"}) {
                affected_rows
            }
        }
    """.replace("$id$",song_id).replace("$name$",data['name']).replace("$date$",str(data['date']))
    print(query)
    result = json.loads(graphQL_client.execute(query))
    if "errors" not in result:
        artist_list = data['artist']
        artist_id_list = []
        for artst in artist_list:
            dc = {}
            # print(json.loads(graphQL_client.execute(artst)))
            artst_id = json.loads(graphQL_client.execute\
                (artist_query(artst)))['data']['artist'][0]['id']
            dc['song_id'] = song_id
            dc['artist_id'] = artst_id
            artist_id_list.append(dc)
        query = song_artist_query()
        json.loads(graphQL_client.execute(query,{'rows':artist_id_list}))
        return True, song_id
        # add entry to song_artist table 
    return False, result['errors'][0]["message"]


def get_song_name(song_id):
    query="""
    {
        songs(where: {id: {_eq: "$a_id$"}}){
            name
        }
    }
    """.replace("$a_id$",song_id)
    return json.loads(graphQL_client.execute(query))['data']['songs'][0]['name']


def get_song_id(song_name):
    query="""
    {
        songs(where: {name: {_eq: "$a_id$"}}){
            id
        }
    }
    """.replace("$a_id$",song_name)
    return json.loads(graphQL_client.execute(query))['data']['songs'][0]['id']
