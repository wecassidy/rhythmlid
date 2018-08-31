"""
Interface with the Rhythmbox library. The MusicLibrary class reads the
Rhythmbox library and builds a list of artists, albums, and songs out
of it.
"""

import os.path
import re
import xml.dom.minidom

class MusicLibrary:
    """
    A data structure to track the state of the music library.

    The library is constructed from Rhythmbox's XML database.
    """

    def __init__(self, db_file):
        """Load the music library into memory from Rhythmbox's library file."""
        self.original_db_file = db_file # Cache the unaltered database filename for communicating with the user
        # Resolve ~user constructs, variables and other potential weirdness
        self.db_file = os.path.realpath(
            os.path.expanduser(
                os.path.expandvars(
                    os.path.normpath(db_file))))

        # Build music library
        self.library = {} # Will be populated with a list of artists
        self.refresh_library()

    def refresh_library(self):
        """Scan the Rhythmbox database and rebuild the library."""
        # Reset library to empty
        self.library = {}

        # Load the XML DOM
        db_dom = xml.dom.minidom.parse(self.db_file)

        # Get the list of database entries
        entries = db_dom.getElementsByTagName("entry")

        # Filter down to a list of songs
        songs = filter(lambda entry: entry.getAttribute("type") == "song", entries)

        # Sort the songs into a list of artists and albums
        for song in songs:
            # Extract song info
            song_info = {}
            for info_node in song.childNodes:
                if isinstance(info_node, xml.dom.minidom.Text): # Skip text nodes at this level
                    continue

                song_info[info_node.nodeName] = info_node.childNodes[0].wholeText

            # Get the artist to classify this song by
            if "album-artist" in song_info: # Use album artist, if available
                artist = song_info["album-artist"]
            else:
                artist = song_info["artist"]

            # Add the track to the library
            if artist not in self.library:
                self.library[artist] = {song_info["album"]: [song_info]}
            elif song_info["album"] not in self.library[artist]:
                self.library[artist][song_info["album"]] = [song_info]
            else:
                self.library[artist][song_info["album"]].append(song_info)

        # Sort albums by disc and track number
        for artist in self.library:
            for album in self.library[artist]:
                # First sort by track number
                self.library[artist][album].sort(key=lambda song: int(song["track-number"]))

                # If there are multiple discs in the album, also sort
                # by disc number.
                if "disc-number" in self.library[artist][album][0]:
                    # This line will not perturb track number order
                    # because list.sort is stable: if two elements
                    # evaluate as equal (as they will when they are on
                    # the same disc) their order will be preserved.
                    self.library[artist][album].sort(key=lambda song: int(song["disc-number"]))

    def artists(self, search=None):
        """Get a list of artists, optionally filtering using a regex."""
        # Collect list of artists
        artists = self.library.keys()

        # Filter down to matches if searching
        if search is not None:
            pattern = re.compile(search)
            artists = filter(lambda a: pattern.search(a), artists)

        return sorted(list(artists))

    def albums(self, search=None):
        """Get a list of albums, optionally filtering using a regex."""
        # Collect list of albums
        albums = []
        for artist in self.library:
            albums.extend(self.library[artist].keys())

        # Filter down to matches if searching
        if search is not None:
            pattern = re.compile(search)
            albums = filter(lambda a: pattern.search(a), albums)

        return sorted(list(albums))

    def songs(self, search=None):
        """Get a list of songs, optionally filtering using a regex."""
        # Collect list of songs
        songs = []
        for artist in self.library:
            for album in self.library[artist]:
                for song in self.library[artist][album]:
                    songs.append(song["title"])

        # Filter down to matches if searching
        if search is not None:
            pattern = re.compile(search)
            songs = filter(lambda a: pattern.search(a), songs)

        return sorted(list(songs))
