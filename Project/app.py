from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

app = Flask(__name__)

app.secret_key = "HOIhkjfaJ4"
app.config['SESSION_COOKIE_NAME'] = 'Aruvs Cookie'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url =  sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for("login", _external=False ))
    sp = spotipy.Spotify(auth = token_info['access_token'])
    all_songs = []
    iteration = 0
    while True:
        items = sp.current_user_saved_tracks(limit = 50, offset = iteration * 50)['items']
        iteration += 1
        all_songs += items
        if (len(items) < 50):
            break
        return str(all_songs)

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="76dff0cbe4d74670bd7a33dc3c4075bc",
        client_secret="1401e59d1b354b849ce38a342f951d14",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read")