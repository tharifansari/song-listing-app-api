import subprocess
from components.hasura_controller import HasuraClient
import hashlib
import json
import uuid
import sys

sys.path.append(".")

graphQL_client = HasuraClient().graphql_client

def get_all_ratings():
    query="""
        {
            rating{
                song_id
                rating
            }
        }
    """
    result = json.loads(graphQL_client.execute(query))
    if "errors" not in result:
        return True, result['data']['rating']
    return False, "query error"

def give_rating(data):
    if "user_id" not in data or "song_id" not in data or "rating" not in data:
        return False, "check the request body, expected keys are not present"
    query = """
        mutation MyMutation {
            insert_rating(objects: {rating: $rating$, user_id: "$user_id$", song_id: "$song_id$" }) {
                affected_rows
            }
        }
    """.replace("$rating$",str(data['rating'])).replace("$song_id$",data['song_id'])\
        .replace("$user_id$",data['user_id'])
    result = json.loads(graphQL_client.execute(query))
    if "errors" not in result:
        return True, "Success"
    return False, result['errors'][0]['message']