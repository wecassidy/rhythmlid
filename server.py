"""
Server-side of a music player that has a web interface. The server
reads the filesystem to determine the contents of the music library
and plays the music through whatever audio interface is available,
while the front-end should handle UI.
"""

import os.path
import re

class MusicLibrary:
    """
    A data structure to track the state of the music library.
    Determines artist, song title, etc. from filenames.

    Expected directory structure:

        music library/
        |- Artist Name/
        |  |- Album Name/
        |  |  |- 01 - Song Title.mp3
        |  |  |- 02 - Song Title.mp3
        |  |  \- ...
        |  \- ...
        \- ...
    """

    TRACK_EXTRACT = re.compile(
        r"(?:.*(?P<disc>\d+)\.)?" # Consume garbage at the start of the name and extract the disc number, if present
        + "(?P<number>\d+)" # Extract track number
        + "(?: - )?" # Consume a hyphen separator if it is present
        + "(?P<title>.*)" # Extract title
        + "\.[\w]+" # Consume the file extension
    )

    def __init__(self, music_dir):
        """
        Load the music library into memory from the filesystem. This
        method will resolve ~user constructs, shell variables, and
        other such path complications before loading the library.
        """

        self.music_dir = music_dir
        # Resolve ~user constructs, variables and other potential weirdness
        self.original_music_dir = self.music_dir # Cache the given version for error messages
        self.music_dir = os.path.normpath(self.music_dir) # Get rid of double slashes
        self.music_dir = os.path.expandvars(self.music_dir) # Expand variables
        self.music_dir = os.path.expanduser(self.music_dir) # Expand ~user constructs
        self.music_dir = os.path.realpath(self.music_dir) # Resolve symlinks

        # Make sure the given library directory is actually a directory
        if not os.path.isdir(self.music_dir):
            raise RuntimeError("Given music directory {} is not a directory".format(self.original_music_dir))

        # Build music library
        self.library = []
        self.refresh_library()

    def refresh_library(self):
        """Scan the filesystem and rebuild the library."""

        self.library = [] # Reset the library

        # Get a list of artists
        artists = os.scandir(self.music_dir)
        for artist in artists:
            if artist.is_dir():
                # Get a list of albums for this artist
                album_list = []

                albums = os.scandir(artist.path)
                for album in albums:
                    if album.is_dir():
                        # Get a list of tracks for the album
                        track_list = []

                        tracks = os.scandir(album.path)
                        for track in tracks:
                            # Extract info from the track filename
                            track_info = MusicLibrary.TRACK_EXTRACT.match(track.name)
                            track_list.append((track_info.group("title"), track.path))

                        album_list.append((album.name, track_list))

                self.library.append((artist.name, album_list))
