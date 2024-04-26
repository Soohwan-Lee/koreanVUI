import os
import struct
import wave
import pyaudio
import time
import io
from pvrecorder import PvRecorder
import pvporcupine
import pvcobra
from pvkoala import create
import whisper
import soundfile as sf
import resampy


### Define hard-coded values here
# Variables for Wake-up word Recognition
access_key = '9x0FaA466xUKn2jZkaAgAakVVBOG7RV6CFf/jI7rCpHJ3NB0HJ3V1w=='
model_path = './resource/speechRecognition/speechRecognitionModule/porcupine_params_ko.pv'
keyword_paths = ['./resource/speechRecognition/speechRecognitionModule/lemmyWakeUp_Mac.ppn']
audio_device_index = -1  # Default audio device
sensitivities = [0.5] * len(keyword_paths)

# Variables for recording (voice activity detection)
speech_threshold = 1.3  # Time of silence after which speech is considered ended

# Variables for Loading Whisper model (Choose: tiny, base, small, medium, (large))
model = whisper.load_model("base")


### Wake-up word Recognition
# Function for wake-up word recognition
def wakeUpWordRecognition():
    recorder = None  # Initialize recorder to None to ensure it's in scope
    porcupine = None  # Similarly for porcupine
    try:
        porcupine = pvporcupine.create(
            access_key=access_key,
            model_path=model_path,
            keyword_paths=keyword_paths,
            sensitivities=sensitivities)
        recorder = PvRecorder(device_index=audio_device_index, frame_length=porcupine.frame_length)
        recorder.start()

        print('LEMMY: Anytime call me ... (press Ctrl+C to exit)')

        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)

            if result >= 0:
                print("LEMMY: Detected wake-up word!")
                break
    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        if recorder:  # Check if recorder was successfully created before deleting
            recorder.delete()
        if porcupine:  # Similarly check porcupine
            porcupine.delete()

    return True



### Recording (Voice Activity Detection)
# Function for recording (voice activity detection)
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
    last_voice_activity_time = time.time()
    timeout_duration = 5  # Timeout for no voice activity

    try:
        while True:
            pcm_data = audio_stream.read(cobra.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * cobra.frame_length, pcm_data)
            voice_activity = cobra.process(pcm)

            current_time = time.time()

            if current_time - last_voice_activity_time > timeout_duration:
                print("No voice activity detected for 5 seconds, reverting to wake-up word recognition.")
                return None

            if voice_activity > 0.3:
                if not recording:
                    print("Your voice started")
                    recording = True
                    frames = []
                last_voice_activity_time = current_time
                frames.append(pcm_data)
            elif recording and current_time - last_voice_activity_time > speech_threshold:
                print("End of voice detected due to silence.")
                break
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        cobra.delete()

    return get_voice_bytes(frames, pa, cobra) if frames else None

# Function to convert frames to byte data
def get_voice_bytes(frames, pa, cobra):
    output = io.BytesIO()
    wf = wave.open(output, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
    wf.setframerate(cobra.sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    output.seek(0)
    return output.read()


### Noise Suppression
# Function for noise suppression
def noise_suppression(byte_data):
    koala = create(access_key=access_key)
    output = io.BytesIO()

    with wave.open(io.BytesIO(byte_data), 'rb') as input_file:
        wf = wave.open(output, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(koala.sample_rate)

        input_length = input_file.getnframes()
        start_sample = 0

        while start_sample < input_length + koala.delay_sample:
            frame_buffer = input_file.readframes(koala.frame_length)
            num_samples_read = len(frame_buffer) // 2
            input_frame = struct.unpack('%dh' % num_samples_read, frame_buffer)

            if num_samples_read < koala.frame_length:
                input_frame += (0,) * (koala.frame_length - num_samples_read)

            output_frame = koala.process(input_frame)

            if start_sample >= koala.delay_sample:
                if start_sample + koala.frame_length > input_length:
                    output_frame = output_frame[:input_length - start_sample]
                wf.writeframes(struct.pack('%dh' % len(output_frame), *output_frame))

            start_sample += koala.frame_length

        wf.close()
    koala.delete()
    output.seek(0)
    return output.read()

### Whisper 모델의 경우 파이썬 프로그램 내에서 오디오 데이터 바로 인식이 안되고 있음...
# import torch

# # Example ShortTensor (replace this with your actual audio data tensor)
# audio_data = torch.ShortTensor(502160)  # Your tensor might be an actual audio data loaded differently

# # Convert ShortTensor to FloatTensor
# audio_data_float = audio_data.float()

# # Define STFT parameters
# n_fft = 400
# hop_length = 160
# win_length = 400
# window = torch.hamming_window(win_length)  # Creating a Hamming window of size 'win_length'

# # Perform the STFT
# spectrogram = torch.stft(
#     audio_data_float, 
#     n_fft=n_fft, 
#     hop_length=hop_length, 
#     win_length=win_length, 
#     window=window, 
#     normalized=False, 
#     return_complex=True
# )

# # Now 'spectrogram' holds the STFT results as a complex tensor


### Whisper: Speech-to-Text
# Function for Speech-to-Text, properly handling byte data with resampling
def speech_to_text(byte_data):
    # Convert byte data to a NumPy array assuming 16-bit PCM audio
    data, current_samplerate = sf.read(io.BytesIO(byte_data), dtype='int16')

    # Whisper models typically expect audio at 16,000 Hz
    target_samplerate = 16000

    # Resample the audio if necessary
    if current_samplerate != target_samplerate:
        data = resampy.resample(data, current_samplerate, target_samplerate)

    # Use the whisper model to transcribe the numpy array
    result = model.transcribe(audio=data)  # Pass the NumPy array directly
    return result['text']

### Main Function
def main():
    wakeUpDetect = False

    while True:
        if not wakeUpDetect:
            wakeUpDetect = wakeUpWordRecognition()
        else:
            audio_bytes = listen_for_voice_and_save()
            if audio_bytes is None:
                wakeUpDetect = False
                continue
            audio_bytes = noise_suppression(audio_bytes)
            transcript = speech_to_text(audio_bytes)
            print(f'Transcript: {transcript}')
            print('===============================')
            wakeUpDetect = False


if __name__ == '__main__':
    main()
