"""
Server-side of a music player that has a web interface. The server
reads the filesystem to determine the contents of the music library
and plays the music through whatever audio interface is available,
while the front-end should handle UI.
"""

import os.path

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
