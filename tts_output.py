# tts_output.py
'''
import os, threading, subprocess

def speak(text):
    # use espeak for low-resource TTS; non-blocking via thread
    def _s(t):
        # escape quotes
        safe = t.replace('"', '\\"')
        cmd = f'espeak "{safe}" --stdout | aplay -q'
        subprocess.call(cmd, shell=True)
    t = threading.Thread(target=_s, args=(text,))
    t.daemon = True
    t.start()
'''
import os

def speak(text):
    # Print text also to terminal so you know it's triggered
    print("🔊 Speaking:", text)

    # Simple, direct espeak call (no threads, guaranteed to run)
    cmd = f'espeak "{text}" --stdout | aplay -q'
    os.system(cmd)

