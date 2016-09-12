# spotisync (name needs work I know)

### Introduction

I've been using Spotify since it was released, back before the mobile apps and back
when the green colour was slightly lighter. One of the things that I hate about modern
Spotify is the way they removed the Starred playlist as a users main playlist in favour
of the "Your Music" model which is pretty much the same thing except it has an "Albums"
and "Artists" view.

I'm a creature of habit and so I still use my Starred playlist as the main container
for all my music on Spotify.

Lately though I've developed a little system. I add a song that I like to Starred,
if it lasts long enough on there without me getting bored of it then I add it to my music.

The problem here was that I regularly added songs accidently by clicking the tick or
added a song to my music and then decided later that I didn't want that song on either
playlist after all etc. Needless to say, maintining these two playlists manually was more
hassle than it was worth.

### Purpose

I decided to write a script to handle this for me. I love Python and a wrapper
exists already for the [Spotify Web API called spotipy](https://github.com/plamere/spotipy). The script is to do some things:

1. The script must detect tracks added to starred that are > 14 days since being added then add them to my music if necessary.

2. Must detect and remove any track in my music that does not appear in Starred. Removed tracks should be stored in a dummy playlist to avoid accidental loss.

### Installation

Currently, I do not plan for this to go beyond me (as it's a pretty specific requirement) so I won't keep a build up to date. If anyone comes upon this and wants to use it however, feel free to clone this repository or download main.py and use the script in any non-commercial way you see fit.

You'll need a python installation (2.7+)

### Usage
Use the following command to run the script:

    python main.py [username]

If your Spotify username is not supplied then the script will prompt for it.

A link will be given, drop that into a web browser, sign in to spotify and then paste the URL that you arrive at back into the script.

Doing this authorises the script to access your spotify playlists, I promise I cannot see and do not care about your spotify credentials.

### Disclaimer

You can use this code and any files any way you want except to make money (I can't imagine how someone would sell this but I'm just saying).

The client ID and secret for my app is visible within this script. Because I couldn't come up with a method to hide it, only obfuscate it, I just decided to leave it in there so please dont abuse it.
