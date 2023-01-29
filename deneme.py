import beepy
import time

sounds = ['coin', 'ping', 'ready']
for sound in sounds:
    print(f"Playing {sound}")
    beepy.beep(sound)
    time.sleep(1)