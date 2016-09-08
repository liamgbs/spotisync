import spotipy
import spotipy.util as sutil

def get_token():
    scope = 'user-library-read user-library-modify'
    user = 'gibbings_lfc'
    clientid = '26637fb0e85141fcb215898a91eb5a84'
    clientsecret = 'c2f01d25d82f4e42941cf1f7e503b643'
    redirecturi = 'https://github.com/liamgbs/spotisync'
    token = sutil.prompt_for_user_token(user, scope, clientid, clientsecret)
    assert token
    return token

sp = spotipy.Spotify(auth=get_token())
