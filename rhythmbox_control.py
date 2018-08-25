"""
A set of wrapper functions around the `rhythmbox-client` command.

Most of the wrappers are extremely thin, but they are nonetheless
useful.
"""

import subprocess

def play():
    return subprocess.run(["rhythmbox-client", "--play"])

def pause():
    return subprocess.run(["rhythmbox-client", "--pause"])

def toggle_play_pause():
    return subprocess.run(["rhythmbox-client", "--play-pause"])

def stop():
    return subprocess.run(["rhythmbox-client", "--stop"])
