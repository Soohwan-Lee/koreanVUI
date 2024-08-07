#!/usr/bin/env python3

import pyaudio
import struct
import time
import pvcobra

from pvrecorder import PvRecorder

pv_access_key= '9x0FaA466xUKn2jZkaAgAakVVBOG7RV6CFf/jI7rCpHJ3NB0HJ3V1w=='

def listen_for_voice():
    cobra = pvcobra.create(access_key=pv_access_key)

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
                rate=cobra.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=cobra.frame_length)

    print("Listening...")

    voice_start = None
    silence_start = None

    while True:
        pcm = audio_stream.read(cobra.frame_length)
        pcm = struct.unpack_from("h" * cobra.frame_length, pcm)
        voice_activity = cobra.process(pcm)

        if voice_activity > 0.3:  # Voice detected
            if voice_start is None:
                voice_start = time.time()
                print(f"Voice started at: {voice_start}")
            silence_start = None
        else:  # No voice detected
            if voice_start is not None and silence_start is None:
                silence_start = time.time()
            elif silence_start is not None and (time.time() - silence_start) > 1.3:
                print(f"End of voice detected at: {time.time()}")
                break

    audio_stream.stop_stream()
    audio_stream.close()
    pa.terminate()
    cobra.delete()

if __name__ == "__main__":
    listen_for_voice()
