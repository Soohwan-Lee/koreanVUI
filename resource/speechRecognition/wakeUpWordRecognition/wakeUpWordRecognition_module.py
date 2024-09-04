import os
import struct
import wave
from pvrecorder import PvRecorder
import pvporcupine

def wakeUpWordRecognition():
    # Define hard-coded values here
    access_key = 'YOUR_API_KEY'
    model_path = './resource/speechRecognition/wakeUpWordRecognition/porcupine_params_ko.pv'
    keyword_paths = ['./resource/speechRecognition/wakeUpWordRecognition/lemmyWakeUp_Mac.ppn']
    audio_device_index = -1  # Default audio device
    sensitivities = [0.5] * len(keyword_paths)

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

    print('Listening ... (press Ctrl+C to exit)')

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)

            if result >= 0:
                print("Detected wake-up word!")
    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        recorder.delete()
        porcupine.delete()

if __name__ == '__main__':
    wakeUpWordRecognition()