# 이 파일은 로컬 저장소에 wav 파일을 임시로 저장하는 모든 과정을 생략함.

import os
import struct
import pyaudio
import time
import numpy as np
from pvrecorder import PvRecorder
import pvporcupine
import pvcobra
from pvkoala import create
import whisper

### Define hard-coded values here
# Variables for Wake-up word Recognition
access_key = 'YOUR_API_KEY'
model_path = './resource/speechRecognition/speechRecognitionModule/porcupine_params_ko.pv'
keyword_paths = ['./resource/speechRecognition/speechRecognitionModule/lemmyWakeUp_Mac.ppn']
audio_device_index = -1  # Default audio device
sensitivities = [0.5] * len(keyword_paths)

# Variables for recording (voice activity detection)
speech_threshold = 1.3

# Variables for Loading Whisper model (Choose: tiny, base, small, medium, (large))
model = whisper.load_model("base")

### Wake-up word Recognition
def wakeUpWordRecognition():
    try:
        porcupine = pvporcupine.create(
            access_key=access_key,
            model_path=model_path,
            keyword_paths=keyword_paths,
            sensitivities=sensitivities)
    except pvporcupine.PorcupineError as e:
        print("Failed to initialize Porcupine: ", e)
        return

    recorder = PvRecorder(device_index=audio_device_index, frame_length=porcupine.frame_length)
    recorder.start()

    print('LEMMY: Anytime call me ... (press Ctrl+C to exit)')
    try:
        while True:
            start_time_wakeUp = time.time()
            pcm = recorder.read()
            result = porcupine.process(pcm)

            if result >= 0:
                print("LEMMY: Detected wake-up word!")
                break
    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        recorder.delete()
        porcupine.delete()
    end_time_wakeUp = time.time()
    print(f"Wake-up word recognition took {round(end_time_wakeUp - start_time_wakeUp, 3)} seconds")
    return True

def listen_for_voice():
    cobra = pvcobra.create(access_key=access_key)
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=cobra.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=cobra.frame_length)

    print("Listening...")
    start_time = time.time()
    timeout = 5
    frames = []

    while True:
        pcm = audio_stream.read(cobra.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * cobra.frame_length, pcm)
        voice_activity = cobra.process(pcm)

        if voice_activity > 0.3:
            start_time_voiceRecording = time.time()
            frames.append(pcm)
            print("Voice started")
            while True:
                pcm = audio_stream.read(cobra.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * cobra.frame_length, pcm)
                voice_activity = cobra.process(pcm)
                frames.append(pcm)

                if voice_activity <= 0.3:
                    if len(frames) > 0:
                        last_voice_time = time.time()
                        while time.time() - last_voice_time <= speech_threshold:
                            pcm = audio_stream.read(cobra.frame_length, exception_on_overflow=False)
                            pcm = struct.unpack_from("h" * cobra.frame_length, pcm)
                            voice_activity = cobra.process(pcm)
                            if voice_activity > 0.3:
                                frames.append(pcm)
                                last_voice_time = time.time()
                            else:
                                frames.append(pcm)

                        print("Voice ended")
                        pcm_data = np.hstack(frames).astype(np.int16)
                        audio_stream.stop_stream()
                        audio_stream.close()
                        pa.terminate()
                        cobra.delete()
                        end_time_voiceRecording = time.time()
                        voiceProcessingTime = end_time_voiceRecording - start_time_voiceRecording
                        print(f"Voice processing time took {round(voiceProcessingTime - speech_threshold, 3)} seconds")
                        return pcm_data
                    else:
                        frames = []
                        break

        if time.time() - start_time > timeout:
            print("No voice detected within the timeout period.")
            audio_stream.stop_stream()
            audio_stream.close()
            pa.terminate()
            cobra.delete()
            return None


### Whisper: Speech-to-Text
def speech_to_text(pcm_data):
    start_time_STT = time.time()
    audio_data = (pcm_data / 32768).astype(np.float32)
    result = model.transcribe(audio=audio_data, fp16=False)
    end_time_STT = time.time()
    print(f"Speech-to-text took {round(end_time_STT - start_time_STT, 3)} seconds")
    return result

### Main Function
def main():
    wakeUpDetect = False
    while True:
        if not wakeUpDetect:
            wakeUpDetect = wakeUpWordRecognition()
        else:
            pcm_data = listen_for_voice()
            if isinstance(pcm_data, np.ndarray):
                result = speech_to_text(pcm_data)
                print(f'Transcript: {result["text"]}')
                print('===============================')
            else:
                print("No voice detected. Going back to wake-up word detection.")
            wakeUpDetect = False

if __name__ == '__main__':
    main()