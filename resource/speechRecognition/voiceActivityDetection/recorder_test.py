# 이 파일은 중간에 잠시라도 말이 끊어지면 발화가 종료된 것으로 인식합니다...
#!/usr/bin/env python3

import pyaudio
import struct
import time
import wave
import pvcobra
import numpy as np

pv_access_key = '9x0FaA466xUKn2jZkaAgAakVVBOG7RV6CFf/jI7rCpHJ3NB0HJ3V1w=='

# Initialize Cobra VAD (Voice Activity Detection)
cobra = pvcobra.create(access_key=pv_access_key)

# PyAudio configuration
pa = pyaudio.PyAudio()
format = pyaudio.paInt16
channels = 1
rate = cobra.sample_rate
frame_length = cobra.frame_length
frames_per_buffer = frame_length

# Open the stream for recording
stream = pa.open(format=format,
                 channels=channels,
                 rate=rate,
                 input=True,
                 frames_per_buffer=frames_per_buffer)

print("Listening...")

is_voice_active = False
voice_frames = []
voice_start_time = None

try:
    while True:
        audio_data = stream.read(frame_length)
        pcm = np.frombuffer(audio_data, dtype=np.int16)

        voice_probability = cobra.process(pcm)
        
        if voice_probability > 0.5:
            if not is_voice_active:
                is_voice_active = True
                voice_start_time = time.time()
                print(f"Voice started at: {voice_start_time}")
            
            voice_frames.append(audio_data)
        else:
            if is_voice_active:
                voice_end_time = time.time()
                print(f"Voice ended at: {voice_end_time}")
                
                # Save the voice_frames to a WAV file
                wav_file_name = f"voice_{int(voice_start_time)}.wav"
                wav_file_name = './resource/speechRecognition/voiceActivityDetection/test.wav'
                wf = wave.open(wav_file_name, 'wb')
                wf.setnchannels(channels)
                wf.setsampwidth(pa.get_sample_size(format))
                wf.setframerate(rate)
                wf.writeframes(b''.join(voice_frames))
                wf.close()

                print(f"Voice saved to {wav_file_name}")
                
                # Reset variables for next voice detection
                is_voice_active = False
                voice_frames = []

except KeyboardInterrupt:
    print("Terminating...")

finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    cobra.delete()
