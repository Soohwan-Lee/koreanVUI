import struct
import wave
import pyaudio
import time
import pvcobra
from pvrecorder import PvRecorder
from pvkoala import create

pv_access_key = '9x0FaA466xUKn2jZkaAgAakVVBOG7RV6CFf/jI7rCpHJ3NB0HJ3V1w=='
output_path = './resource/speechRecognition/noiseSuppression/testSample_withoutNoise.wav'
speech_threshold = 1.3  # Adjust this value as needed

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
    last_voice_time = None

    koala = create(access_key=pv_access_key)

    # Ensure output file sample rate matches the Koala's sample rate
    with wave.open(output_path, 'wb') as output_file:
        output_file.setnchannels(1)
        output_file.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        output_file.setframerate(koala.sample_rate)

        frame_buffer = bytearray()

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
                    if voice_start is not None and last_voice_time is not None:
                        elapsed_time = time.time() - last_voice_time
                        if elapsed_time > speech_threshold:
                            print("Voice ended")
                            break
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

# Uncomment to run the function
if __name__ == "__main__":
    listen_for_voice()



### 아래 코드는 동작은 하나 sample rate가 맞지 않음.
# import struct
# import wave
# import pyaudio
# import time
# import pvcobra
# from pvrecorder import PvRecorder
# from pvkoala import create

# pv_access_key = '9x0FaA466xUKn2jZkaAgAakVVBOG7RV6CFf/jI7rCpHJ3NB0HJ3V1w=='
# output_path = './resource/speechRecognition/noiseSuppression/testSample_withoutNoise.wav'
# speech_threshold = 1.3  # Adjust this value as needed

# def listen_for_voice():
#     cobra = pvcobra.create(access_key=pv_access_key)
#     pa = pyaudio.PyAudio()
#     audio_stream = pa.open(
#         rate=cobra.sample_rate,
#         channels=1,
#         format=pyaudio.paInt16,
#         input=True,
#         frames_per_buffer=cobra.frame_length)

#     print("Listening...")
#     voice_start = None
#     last_voice_time = None

#     koala = create(access_key=pv_access_key)

#     with wave.open(output_path, 'wb') as output_file:
#         output_file.setnchannels(1)
#         output_file.setsampwidth(2)  # Assuming 16-bit PCM
#         output_file.setframerate(koala.sample_rate)

#         while True:
#             try:
#                 pcm = audio_stream.read(cobra.frame_length, exception_on_overflow=False)
#                 pcm = struct.unpack_from("h" * cobra.frame_length, pcm)
#                 voice_activity = cobra.process(pcm)

#                 if voice_activity > 0.3:
#                     # Voice detected
#                     if voice_start is None:
#                         voice_start = time.time()
#                         print("Voice started")
#                     last_voice_time = time.time()

#                     # Adjust the input frame to match Koala's frame length
#                     if len(pcm) < koala.frame_length:
#                         pcm = pcm + (0,) * (koala.frame_length - len(pcm))
#                     elif len(pcm) > koala.frame_length:
#                         pcm = pcm[:koala.frame_length]

#                     # Perform noise suppression
#                     enhanced_frame = koala.process(pcm)
#                     output_file.writeframes(struct.pack(f'{len(enhanced_frame)}h', *enhanced_frame))
#                 else:
#                     # No voice detected
#                     if voice_start is not None and last_voice_time is not None:
#                         elapsed_time = time.time() - last_voice_time
#                         if elapsed_time > speech_threshold:
#                             print("Voice ended")
#                             break
#             except IOError as e:
#                 if e.errno == pyaudio.paInputOverflowed:
#                     print("Input overflowed. Skipping frame...")
#                     continue
#                 else:
#                     raise e

#     audio_stream.stop_stream()
#     audio_stream.close()
#     pa.terminate()
#     cobra.delete()
#     koala.delete()

# if __name__ == "__main__":
#     listen_for_voice()