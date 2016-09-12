import spotipy
import spotipy.util as sutil
import sys
from datetime import datetime


class AuthException(Exception):
    pass


class TrackPresentException(Exception):
    pass


def get_username():
    if len(sys.argv) > 1:
        user = sys.argv[1]
    else:
        user = raw_input("Enter your username: ")
    return user


def get_token(user):
    scope = 'playlist-modify-private'
    clientid = '26637fb0e85141fcb215898a91eb5a84'
    clientsecret = 'c2f01d25d82f4e42941cf1f7e503b643'
    redirecturi = 'http://example.com/callback/'
    token = sutil.prompt_for_user_token(user, scope, clientid,
                                        clientsecret, redirecturi)
    if not token:
        raise AuthException("Auth Token Failed")
    else:
        return token


def get_starred_tracks(sp, user):
    starred = sp.user_playlist(user)  # get starred playlist
    tracks_paging = starred['tracks']  # extract paging object
    tracklist = []
    while tracks_paging:
        star_tracks = tracks_paging['items']  # tracks as playlist track object
        for playlist_track in star_tracks:
            tracklist.append((playlist_track['added_at'],
                              playlist_track['track']['id']))
        tracks_paging = sp.next(tracks_paging)
    return tracklist


def get_my_music_tracks(sp):
    limit, offset = 50, 0
    tracklist = []
    my_music = sp.current_user_saved_tracks(limit, offset)
    while my_music['items']:  # while tracks are being returned
        for playlist_track in my_music['items']:
            tracklist.append((playlist_track['added_at'],
                              str(playlist_track['track']['id'])))
        offset += 50
        my_music = sp.current_user_saved_tracks(limit, offset)
    return tracklist


def is_track_older_than(track, age_days=14):
    assert isinstance(track, tuple)
    spotify_format = "%Y-%m-%dT%H:%M:%SZ"

    # convert unicode to python datetime object
    track_date = datetime.strptime(track[0], spotify_format)
    # if delta of todays date and track add date > 7
    if (datetime.now() - track_date).days > age_days:
        return True
    else:
        return False


def get_old_starred(sp, user):
    starred_tracks = get_starred_tracks(sp, user)
    for track in starred_tracks:
        # if track is new then ignore
        if not is_track_older_than(track):
            starred_tracks.remove(track)
    return starred_tracks


def get_unsynced(track_list_one, track_list_two):
    t1, t2 = [], []
    t1 = [x[1] for x in track_list_one]
    t2 = [x[1] for x in track_list_two]
    unsynced = set(t1).difference(set(t2))

    # remove all None values (for old playlists)
    unsynced = [x for x in unsynced if x is not None]
    return list(unsynced)


def get_playlist_id_by_name(sp, user, playlist_name):
    playlists = sp.user_playlists(user)['items']
    for pl in playlists:
        if pl['name'] == playlist_name:
            return pl['id']
    return None


def get_stash_playlist_id(sp, user, stash_name='spotisync'):
    stash_id = get_playlist_id_by_name(sp, user, stash_name)
    # if stash playlist doesnt exist
    if stash_id is None:
        sp.user_playlist_create(user, stash_name, public=False)
        return get_playlist_id_by_name(sp, user, stash_name)
    else:
        return stash_id


def sync_with_starred(sp, unsynced):
    # if list is empty, no tracks to sync
    if len(unsynced) == 0:
        print "No new tracks to add from starred"
        return

    if True in sp.current_user_saved_tracks_contains(unsynced):
        raise TrackPresentException("ERROR: Track already present")
    else:
        print "Adding %i tracks to your music..." % len(unsynced)
        sp.current_user_saved_tracks_add(unsynced)
        print "Done."


def sync_with_music(sp, user, unsynced):
    if len(unsynced) == 0:
        print "No new tracks to stash and remove from music."
        return

    stash_id = get_stash_playlist_id(sp, user)
    print "Stashing & removing %i tracks from your music..." % len(unsynced)
    sp.user_playlist_add_tracks(user, stash_id, unsynced)
    sp.current_user_saved_tracks_delete(unsynced)
    print "Done."


def main():
    # Auth
    user = get_username()
    sp = spotipy.Spotify(auth=get_token(user))
    # Get all tracks needed
    my_music_tracks = get_my_music_tracks(sp)
    starred_tracks = get_old_starred(sp, user)
    # Add old starred tracks to my music
    unsynced_with_starred = get_unsynced(starred_tracks, my_music_tracks)
    sync_with_starred(sp, unsynced_with_starred)
    # Stash and remove tracks in my music that dont appear in starred
    unsynced_with_music = get_unsynced(my_music_tracks, starred_tracks)
    sync_with_music(sp, user, unsynced_with_music)

if __name__ == "__main__":
    main()
