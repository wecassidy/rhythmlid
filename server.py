import os.path

MUSIC_DIR = "~/Music"

# Resolve ~user constructs, variables and other potential weirdness
MUSIC_DIR = os.path.normpath(MUSIC_DIR) # Get rid of double slashes
MUSIC_DIR = os.path.expandvars(MUSIC_DIR) # Expand variables
MUSIC_DIR = os.path.expanduser(MUSIC_DIR) # Expand ~user constructs
MUSIC_DIR = os.path.realpath(MUSIC_DIR) # Resolve symlinks
