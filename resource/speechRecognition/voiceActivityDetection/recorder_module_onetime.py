import pyaudio
import struct
import time
import wave
import pvcobra

access_key = '9x0FaA466xUKn2jZkaAgAakVVBOG7RV6CFf/jI7rCpHJ3NB0HJ3V1w=='
speech_threshold = 1.3  # Duration to recognize the end of speech

def listen_for_voice_and_save():
    cobra = pvcobra.create(access_key=access_key)
    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
                rate=cobra.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=cobra.frame_length)

    print("Listening...")

    recording = False
    frames = []
    last_voice_activity_time = None
    end_of_speech_detected = False

    try:
        while not end_of_speech_detected:
            pcm_data = audio_stream.read(cobra.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * cobra.frame_length, pcm_data)
            voice_activity = cobra.process(pcm)

            current_time = time.time()

            if voice_activity > 0.3:
                if not recording:
                    print("Voice started")
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

def save_voice(frames, pa, cobra):
    file_name = './resource/speechRecognition/voiceActivityDetection/test.wav'
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
    wf.setframerate(cobra.sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Voice saved to {file_name}")

if __name__ == "__main__":
    listen_for_voice_and_save()
