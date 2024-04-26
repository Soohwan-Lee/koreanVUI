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
input_path = file_path + 'sample.wav'
output_path = file_path + 'sample_withoutNoise.wav'

# Variables for Loading Whisepr model (Choose: tiny, base, small, medium, (large))
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


### Recording (Voice Activity Detection)
def listen_for_voice_and_save():
    cobra = pvcobra.create(access_key=access_key)
    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
                rate=cobra.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=cobra.frame_length)

    print("LEMMY: Listening...")

    recording = False
    frames = []
    last_voice_activity_time = time.time()  # Initialize to current time
    end_of_speech_detected = False
    timeout_duration = 5  # 5 seconds timeout for no voice activity

    try:
        while not end_of_speech_detected:
            pcm_data = audio_stream.read(cobra.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * cobra.frame_length, pcm_data)
            voice_activity = cobra.process(pcm)

            current_time = time.time()

            # Check for timeout due to no voice activity
            if current_time - last_voice_activity_time > timeout_duration and not recording:
                print("No voice activity detected for 5 seconds, reverting to wake-up word recognition.")
                break

            if voice_activity > 0.3:
                if not recording:
                    start_time_recording = current_time
                    print("Your voice started")
                    recording = True
                    frames = []  # Reset the frame buffer when a new voice starts
                last_voice_activity_time = current_time
                frames.append(pcm_data)
            elif recording and last_voice_activity_time is not None:
                if current_time - last_voice_activity_time > speech_threshold:
                    print(f"End of voice detected due to {speech_threshold} seconds of silence")
                    end_of_speech_detected = True
    finally:
        if frames:
            save_voice(frames, pa, cobra)
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        cobra.delete()
        if not end_of_speech_detected:  # Add a return value to signal the need to revert to wake-up word listening
            return False
    return True  # If end of speech was detected successfully


# Saving recorded voice
def save_voice(frames, pa, cobra):
    file_name = file_path + 'sample.wav'
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
    wf.setframerate(cobra.sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()


### Noise Suppression
# Function for noise suppression
def noise_suppression():
    start_time_suppression = time.time()
    try:
        koala = create(access_key=access_key)

        with wave.open(input_path, 'rb') as input_file:
            if input_file.getframerate() != koala.sample_rate or input_file.getnchannels() != 1 or input_file.getsampwidth() != 2:
                raise ValueError('Invalid WAV file format for Koala')

            input_length = input_file.getnframes()
            with wave.open(output_path, 'wb') as output_file:
                output_file.setnchannels(1)
                output_file.setsampwidth(2)
                output_file.setframerate(koala.sample_rate)

                start_sample = 0
                while start_sample < input_length + koala.delay_sample:
                    frame_buffer = input_file.readframes(koala.frame_length)
                    num_samples_read = len(frame_buffer) // 2  # 2 bytes per sample (16-bit PCM)
                    input_frame = struct.unpack('%dh' % num_samples_read, frame_buffer)
                    
                    if num_samples_read < koala.frame_length:
                        input_frame += (0,) * (koala.frame_length - num_samples_read)
                    
                    output_frame = koala.process(input_frame)

                    if start_sample >= koala.delay_sample:
                        if start_sample + koala.frame_length > input_length:
                            output_frame = output_frame[:input_length - start_sample]
                        output_file.writeframes(struct.pack('%dh' % len(output_frame), *output_frame))
                    
                    start_sample += koala.frame_length

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        koala.delete()
    end_time_suppression = time.time()
    print(f"Noise suppression took {round(end_time_suppression - start_time_suppression, 3)} seconds")


### Whisper: Speech-to-Text
# Function for Speech-to-Text
def speech_to_text():
    start_time_STT = time.time()
    # Transcribe the audio file to text
    result = model.transcribe(file_path + 'sample_withoutNoise.wav', fp16=False)
    end_time_STT = time.time()
    print(f"Speech-to-text took {round(end_time_STT - start_time_STT,3)} seconds")
    return result

### Main Function modification to handle the new return from listen_for_voice_and_save()
def main():
    wakeUpDetect = False  # Wake-up word detection state

    while True:
        if not wakeUpDetect:
            wakeUpDetect = wakeUpWordRecognition()
        else:
            if not listen_for_voice_and_save():  # If the function returns False, reset wakeUpDetect
                wakeUpDetect = False
                continue
            noise_suppression()
            result = speech_to_text()
            print(f'Transcript: {result["text"]}')
            print('===============================')
            wakeUpDetect = False  # Reset for the next cycle


if __name__ == '__main__':
    main()