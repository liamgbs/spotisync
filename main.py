import spotipy
import spotipy.util as sutil
import sys

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
    tracks = tracks_paging['items'] # return list containing all tracks as playlist track objects
    return tracks

def main():
    user = get_username()
    sp = spotipy.Spotify(auth=get_token(user))
    starred_tracks = get_starred_tracks(sp, user)
    print starred_tracks


if __name__ == "__main__" : main()
