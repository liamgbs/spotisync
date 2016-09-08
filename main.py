import spotipy
import spotipy.util as sutil
import sys
from datetime import datetime, timedelta
from pprint import pprint

def get_username():
    if len(sys.argv) > 1:
        user = sys.argv[1]
    else:
        user = raw_input("Enter your username: ")
    return user

def get_token(user):
    scope = 'playlist-read-private'
    clientid = '26637fb0e85141fcb215898a91eb5a84'
    clientsecret = 'c2f01d25d82f4e42941cf1f7e503b643'
    redirecturi = 'http://example.com/callback/'
    token = sutil.prompt_for_user_token(user, scope, clientid, clientsecret, redirecturi)
    assert token
    return token

def get_starred_tracks(sp, user):
    starred = sp.user_playlist(user) # get starred playlist
    tracks_paging = starred['tracks'] # extract paging object
    tracklist = []
    while tracks_paging:
        star_tracks = tracks_paging['items'] # list containing all tracks as playlist track objects
        for playlisttrack in star_tracks:
            tracklist.append( (playlisttrack['added_at'], str(playlisttrack['track']['id']), playlisttrack['track']['name']) )
        tracks_paging = sp.next(tracks_paging)
    return tracklist

def is_track_older_than(track, age_days=7):
    assert isinstance(track, tuple)
    spotify_format = "%Y-%m-%dT%H:%M:%SZ"
    track_date = datetime.strptime(track[0], spotify_format)
    if not (datetime.now() - track_date).days > age_days: # if delta of todays date and track add date > 7 (?)
        return True
    else:
        return False

def main():
    user = get_username()
    sp = spotipy.Spotify(auth=get_token(user))
    starred_tracks = get_starred_tracks(sp, user)

    for t in starred_tracks:
        print t[2]
        print is_track_older_than(t)
    print len(starred_tracks)

if __name__ == "__main__" : main()
