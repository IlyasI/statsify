import json

from flask import (Flask, request, redirect, render_template, url_for, session)
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
import spotipy
import spotipy.oauth2

app = Flask(__name__)
app.secret_key = "YOUR OWN SECRET KEY HERE"
bootstrap = Bootstrap(app)

# Flask Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8000
REDIRECT_URI = "{}:{}/topartists".format(CLIENT_SIDE_URL, PORT)

SCOPE = ("user-top-read")

TEMPLATES_AUTO_RELOAD = True
SEND_FILE_MAX_AGE_DEFAULT = 0

@app.route("/")
def index():
    """Redirect user to Spotify login/auth."""
    sp_oauth = get_oauth()
    return redirect(sp_oauth.get_authorize_url())

@app.route("/toptracks")
def display_top_tracks():
    if request.args.get("code"):
        get_spotify(request.args["code"])

    """render users top tracks"""
    #playlist_url = make_top_playlist()
    top_tracks_short = get_user_top_tracks(time_range='short_term')
    top_tracks_med = get_user_top_tracks(time_range='medium_term')
    top_tracks_long = get_user_top_tracks(time_range='long_term')
    session["track_names_long"] = [track["name"] for track in top_tracks_long]
    session["track_names_med"] = [track["name"] for track in top_tracks_med]
    session["track_names_short"] = [track["name"] for track in top_tracks_short]

    return render_template("toptracks.html", top_tracks_long=top_tracks_long, top_tracks_med = top_tracks_med, top_tracks_short=top_tracks_short)

@app.route("/topartists")
def display_top_artists():
    """render users top artists"""
    # This is the route which the Spotify OAuth redirects to.
    # We finish getting an access token here.
    if request.args.get("code"):
        get_spotify(request.args["code"])

    top_artists_short = get_user_top_artists(time_range='short_term', limit=50)
    top_artists_med = get_user_top_artists(time_range='medium_term', limit=50)
    top_artists_long = get_user_top_artists(time_range='long_term', limit=50)
    session["artist_names_long"] = [artist["name"] for artist in top_artists_long]
    session["artist_names_med"] = [artist["name"] for artist in top_artists_med]
    session["artist_names_short"] = [artist["name"] for artist in top_artists_short]

    return render_template("topartists.html", top_artists_long=top_artists_long, top_artists_med = top_artists_med, top_artists_short=top_artists_short)

def get_oauth():
    """Return a Spotipy Oauth2 object."""
    prefs = get_prefs()
    return spotipy.oauth2.SpotifyOAuth(
        prefs["ClientID"], prefs["ClientSecret"], REDIRECT_URI, scope=SCOPE,
        cache_path=".tokens")

def get_spotify(auth_token=None):
    """Return an authenticated Spotify object."""
    oauth = get_oauth()
    token_info = oauth.get_cached_token()
    if not token_info and auth_token:
        token_info = oauth.get_access_token(auth_token)
    return spotipy.Spotify(auth=token_info["access_token"])

def get_prefs():
    with open("config.json") as prefs_file:
        prefs = json.load(prefs_file)

    return prefs

def get_names(tracks):
    """Return just the name component of a list of name/id tuples."""
    return [track[0] for track in tracks]

def get_user_playlists():
    """Return an id, name, images tuple of a user's playlists."""
    sp = get_spotify()
    user_id = sp.current_user()["id"]
    results = sp.user_playlists(user_id)

    playlists = results["items"]
    while results["next"]:
        results = sp.next(results)
        playlists.extend(results["items"])

    playlist_names = [{"id": playlist["id"], "name": playlist["name"],
                       "images": playlist["images"]} for playlist in playlists]

    return playlist_names

#BROKEN
# def make_top_playlist(time_range='medium_term'):
#     sp = get_spotify()
#     sp.trace = False
#     user_id = sp.current_user()["id"]
#     results = sp.current_user_top_tracks(offset = 0, limit = 50, time_range = time_range)
#     tracks = results["items"]
#     new_playlist_name = "My Top Tracks"
#     sp.user_playlist_create(user_id, new_playlist_name)
#     new_playlist_id = get_playlist_id_by_name(new_playlist_name)
#     while results["next"]:
#         results = sp.next(results)
#         tracks.extend(results["items"])
#
#     track_ids = [track["id"] for track in tracks]
#
#     for ids in track_ids:
#         sp.user_playlist_add_tracks(user_id, new_playlist_id, ids)
#     playlist_url = sp.user_playlist(user_id, new_playlist_id)["external_urls"]["spotify"]
#     return playlist_url

#BROKEN
# def get_user_recently_played(limit=50):
#     sp = get_spotify()
#     sp.trace = False
#     user_id = sp.current_user()["id"]
#     results = sp.current_user_recently_played(limit)
#
#     recent_tracks = results["items"]
#     while results["next"]:
#         results = sp.next(results)
#         recent_tracks.extend(results["items"])
#
#     recent_tracks = [{"played_at": track["played_at"], "id": track["track"]["id"],
#                       "name": track["track"]["name"], "artists": track["track"]["artists"] for track in recent_tracks}]

def get_user_top_artists(limit=50, time_range='medium_term'):
    sp = get_spotify()
    sp.trace = False
    user_id = sp.current_user()["id"]
    results = sp.current_user_top_artists(offset = 0, limit = limit, time_range = time_range)

    artists = results["items"]
    while results["next"]:
        results = sp.next(results)
        artists.extend(results["items"])

    artist_names = [{"id": artist["id"], "name": artist["name"],
                    "images": artist["images"], "genres": artist["genres"],
                    "popularity": artist["popularity"]} for artist in artists]

    return artist_names

def get_user_top_tracks(limit=50, time_range='medium_term'):
    sp = get_spotify()
    sp.trace = False
    user_id = sp.current_user()["id"]
    results = sp.current_user_top_tracks(offset = 0, limit = limit, time_range = time_range)

    tracks = results["items"]
    #commented out as it was affecting performance. For some reason spotify returns a whole lot more for medium-term
    #while results["next"]:
    #    results = sp.next(results)
    #    tracks.extend(results["items"])

    track_names = [{"id": track["id"], "name": track["name"], "popularity": track["popularity"],
                    "album_images": track["album"]["images"], "album_name": track["album"]["name"],
                    "explicit": track["explicit"], "artist_name": track["artists"][0]["name"],
                    "artist_id": track["artists"][0]["id"], "album_id": track["album"]["id"]} for track in tracks]

    return track_names

def get_playlist_id_by_name(name):
    """Return the id for a playlist with name: 'name'."""
    return [playlist["id"] for playlist in get_user_playlists() if
            playlist["name"] == name][0]


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
