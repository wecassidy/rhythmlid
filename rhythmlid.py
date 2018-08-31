"""
Server-side of a web interface to the Rhythmbox music player.

The server parses the Rhythmbox database to determine library
information, then delivers albums, etc. to the web client to display.
Playback is handled by an instance of Rhythmbox on the server
computer.
"""

from flask import Flask, render_template, url_for, redirect
from rhythmbox_library import MusicLibrary

# Start the app
app = Flask(__name__)

# Load the library
ml = MusicLibrary("~/.local/share/rhythmbox/rhythmdb.xml")

@app.route("/")
def rhythmlid():
    return render_template("player.j2", ml=ml)
