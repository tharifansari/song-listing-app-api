import subprocess
from components.hasura_controller import HasuraClient
import hashlib
import json
import uuid
import sys

sys.path.append(".")

graphQL_client = HasuraClient().graphql_client


def make_md5_hash(user_entered_password):
    result = hashlib.md5(user_entered_password.encode()) 
    password_hash = result.hexdigest()
    return password_hash


def get_userid_password(mail):
    query = """
        {
            user(where: {email: {_eq: "$mail$"}}){
                id
                password
                name
            }
        }
    """.replace("$mail$",str(mail))
    user_details = json.loads(graphQL_client.execute(query))['data']['user']    
    return user_details


def validate_login(data):
    mail = data['mail']
    password = make_md5_hash(data['password'])
    userid_password = get_userid_password(mail)
    if userid_password == []:
        return False, "Email doesn't belong to a user"
    user_password = userid_password[0]['password']
    user_details = {
        "id" : userid_password[0]['id'],
        "name" : userid_password[0]['name']
    }
    if password != user_password:
        return False, "Wrong password"
    return True, user_details
    

def sign_up(data):
    mail = data['mail']
    name = data['name']
    password = make_md5_hash(data['password'])
    query = """
        {
            user(where: {email: {_eq: "$mail$"}}){
                id
            }
        }
    """.replace("$mail$",str(mail))
    check_user = json.loads(graphQL_client.execute(query))['data']['user']
    if check_user != []:
        return False, "User already exist"
    user_id = str(uuid.uuid4())
    query = '''
        mutation MyMutation
        {
            insert_user(objects: {id: "$uid$", name: "$name$", email: "$email$", password: "$password$" }) {
                affected_rows
            }
        }
        '''.replace('$email$', mail).replace('$uid$', str(user_id))
    
    query = query.replace('$password$', password).replace('$name$', name)
    print(json.loads(graphQL_client.execute(query)))
    
    return True, user_id
