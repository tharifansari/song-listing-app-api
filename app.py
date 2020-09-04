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
    if request.method == "GET":
        top = request.args.get('top', default=-1, type=int)
        songs_status, all_songs = songs.get_all_songs()
        if songs_status != True:
            return all_songs, 400
        if top!=-1 :
            if top<=0:
                return "Send a valid top value", 400
            top_status, top_songs =  songs.top_songs(all_songs, top) 
            if top_status != True:
                return top_songs, 400
            top_song_list = []
            for d in all_songs:
                if d['id'] in top_songs:
                    top_song_list.append(d)
            return json.dumps(top_song_list), 200
        return json.dumps(all_songs), 200
    elif request.method == "POST":
        data = request.json
        add_song_status, msg = songs.add_song(data)
        if add_song_status != True:
            return msg,400
        return msg,200
    


@app.route("/artist", methods=["POST","GET"])
def get_artist():
    if request.method == "GET":
        top = request.args.get('top', default=-1, type=int)
        artist_status, all_artist = artist.get_all_artist()
        if artist_status != True:
            return all_artist, 400
        if top!=-1 :
            if top<=0:
                return "Send a valid top value", 400
            top_status, top_songs =  artist.top_artist(all_artist, top) 
            if top_status != True:
                return top_songs, 400
            top_artist_list = []
            for d in all_artist:
                if d['id'] in top_songs:
                    top_artist_list.append(d)
            return json.dumps(top_artist_list), 200
        return json.dumps(all_artist), 200
    elif request.method == "POST":
        data = request.json
        add_song_status, msg = artist.add_artist(data)
        if add_song_status != True:
            return msg,400
        return msg,200

@app.route("/artist/<song_id>", methods=["GET"])
def artiist_for_id(song_id):
    artist_ls = artist.get_artist_song(song_id)
    artist_dc = {}
    for artst in artist_ls:
        artist_dc[artst] = artist.get_artist_name(artst)
    return json.dumps(artist_dc)

@app.route("/song/<artist_id>",methods=["GET"])
def songs_for_artist(artist_id):
    songs_ls = artist.get_song_artist(artist_id)
    song_dc = {}
    for sng in songs_ls:
        song_dc[sng] = songs.get_song_name(sng)
    return json.dumps(song_dc)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
