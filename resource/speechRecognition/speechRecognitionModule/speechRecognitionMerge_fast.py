# 이 파일은 voice detection -> recording -> save&load -> noise_suppression 과정에서 voice detection 후 곧바로 noise suppression을 하며 save하도록 구성됨.
# 단, noise suppression 후에는 wav 파일을 저장했다가 다시 불러 와서 whisper를 통해 STT 시작.

import os
import struct
import wave
import pyaudio
import time
import wave
from pvrecorder import PvRecorder
import pvporcupine
import pvcobra
from pvkoala import create
import whisper
import numpy as np


### Define hard-coded values here
# Variables for Wake-up word Recognition
access_key = '9x0FaA466xUKn2jZkaAgAakVVBOG7RV6CFf/jI7rCpHJ3NB0HJ3V1w=='
model_path = './resource/speechRecognition/speechRecognitionModule/porcupine_params_ko.pv'
keyword_paths = ['./resource/speechRecognition/speechRecognitionModule/lemmyWakeUp_Mac.ppn']
audio_device_index = -1  # Default audio device
sensitivities = [0.5] * len(keyword_paths)

# Variables for recording (voice activity detection)
speech_threshold = 1.3      # 이 시간 이상으로 발화가 멈추면 발화 종료로 인식
file_path = './resource/speechRecognition/speechRecognitionModule/'

# Variables for noise suppression
output_path = file_path + 'sample_withoutNoise.wav'

# Variables for Loading Whisper model (Choose: tiny, base, small, medium, (large))
model = whisper.load_model("base")


### Wake-up word Recognition
# Function for wake-up word recognition
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
            start_time_first = time.time()
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
    print(f"Wake-up word recognition took {round(end_time_wakeUp - start_time_first, 3)} seconds")
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
    voice_start = None
    last_voice_time = None
    timeout = 5  # Timeout in seconds

    koala = create(access_key=access_key)

    # Ensure output file sample rate matches the Koala's sample rate
    with wave.open(output_path, 'wb') as output_file:
        output_file.setnchannels(1)
        output_file.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        output_file.setframerate(koala.sample_rate)

        frame_buffer = bytearray()
        start_time = time.time()

        while True:
            try:
                pcm = audio_stream.read(cobra.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * cobra.frame_length, pcm)
                voice_activity = cobra.process(pcm)

                if voice_activity > 0.3:
                    # Voice detected
                    if voice_start is None:
                        voice_start = time.time()
                        print("Voice started")
                    last_voice_time = time.time()

                    # Add to buffer
                    frame_buffer.extend(struct.pack('h' * len(pcm), *pcm))

                    # Check buffer length and process if it matches Koala's frame length
                    while len(frame_buffer) >= koala.frame_length * 2:  # 2 bytes per sample (16-bit)
                        # Extract the portion of the buffer to process
                        frame_to_process = frame_buffer[:koala.frame_length * 2]
                        frame_buffer = frame_buffer[koala.frame_length * 2:]

                        # Convert bytes back to short ints
                        frame_to_process = struct.unpack(f'{koala.frame_length}h', frame_to_process)

                        # Perform noise suppression
                        enhanced_frame = koala.process(frame_to_process)
                        output_file.writeframes(struct.pack(f'{len(enhanced_frame)}h', *enhanced_frame))
                else:
                    # No voice detected
                    if voice_start is None and time.time() - start_time > timeout:
                        print("No voice detected within the timeout period.")
                        return False
                    elif voice_start is not None and last_voice_time is not None:
                        elapsed_time = time.time() - last_voice_time
                        if elapsed_time > speech_threshold:
                            print("Voice ended")
                            processing_time = time.time() - voice_start - speech_threshold
                            print(f"Voice processing time (excluding speech_threshold): {round(processing_time, 3)} seconds")
                            return True
            except IOError as e:
                if e.errno == pyaudio.paInputOverflowed:
                    print("Input overflowed. Skipping frame...")
                    continue
                else:
                    raise e

    audio_stream.stop_stream()
    audio_stream.close()
    pa.terminate()
    cobra.delete()
    koala.delete()


### Whisper: Speech-to-Text
# Function for Speech-to-Text
def speech_to_text():
    start_time_STT = time.time()
    # Transcribe the audio file to text
    result = model.transcribe(output_path, fp16=False)
    end_time_STT = time.time()
    print(f"Speech-to-text took {round(end_time_STT - start_time_STT, 3)} seconds")
    return result


### Main Function
def main():
    wakeUpDetect = False      # Wake-up word 감지

    while True:
        if wakeUpDetect is False:
            wakeUpDetect = wakeUpWordRecognition()
        else:
            voice_detected = listen_for_voice()
            if voice_detected:
                result = speech_to_text()
                print(f'Transcript: {result["text"]}')
                print('===============================')
            else:
                print("No voice detected. Going back to wake-up word detection.")
            wakeUpDetect = False        # GPT와 연결시 위치 조정


if __name__ == '__main__':
    main()