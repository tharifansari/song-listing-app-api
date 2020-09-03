from flask import Flask, Response, redirect, request, session, url_for
from components import artist, login, ratings, songs
import uuid
import json

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

PORT = 8000


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    user_signup_status, msg =  login.sign_up(data)    
    if user_signup_status != True:
        return msg, 400
    return msg, 200
    # session['userid'] = msg
    # return "cool buddy {}".format(session['userid']), 200


@app.route("/login", methods=["GET"])
def user_login():
    data = request.json
    user_login_status, msg =  login.validate_login(data)
    print(user_login_status)
    if user_login_status != True:
        return msg, 400
    return msg['id'], 200
    # print(msg)
    # session['userid'] = msg['id']
    # return "cool {} {}".format(msg['name'],session['userid']), 200
    

@app.route("/rating", methods=["GET","POST"])
def get_review():
    # filter for songs and filter for artist
    if request.method == "GET":
        check_rating, all_rating = ratings.get_all_ratings()
        if check_rating!=True:
            return all_rating, 400
        return json.dumps(all_rating), 200
    elif request.method == "POST":
        data = request.json
        # user_id song_id rating
        set_rating_status, msg = ratings.give_rating(data)
        if set_rating_status != True:
            return msg, 400
        return msg, 200
    


@app.route("/song", methods=["POST","GET"])
def get_song():
    top = request.args.get('top', default=-1, type=int)
    # use url filter as top and validate the top
    pass


@app.route("/artist", methods=["POST","GET"])
def get_artist():
    # use url filter as top and validate the top
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
