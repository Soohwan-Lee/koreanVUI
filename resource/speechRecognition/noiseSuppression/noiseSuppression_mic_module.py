import struct
import wave
from pvkoala import create
from pvrecorder import PvRecorder

# Settings
access_key = 'YOUR_API_KEY'  # Replace with your actual Picovoice access key
output_path = './resource/speechRecognition/noiseSuppression/testSample_withoutNoise.wav'  # Path where the output will be saved

def noise_suppression():
    try:
        # Initialize the Koala noise suppressor and the recorder
        koala = create(access_key=access_key)
        recorder = PvRecorder(device_index=-1, frame_length=koala.frame_length)

        # Setup the WAV file for writing the processed audio
        with wave.open(output_path, 'wb') as output_file:
            output_file.setnchannels(1)
            output_file.setsampwidth(2)  # Assuming 16-bit PCM
            output_file.setframerate(koala.sample_rate)

            print('Recording and processing... Press Ctrl+C to stop.')
            recorder.start()

            # Continuously read, process, and write frames
            while True:
                frame = recorder.read()
                enhanced_frame = koala.process(frame)
                output_file.writeframes(struct.pack(f'{len(enhanced_frame)}h', *enhanced_frame))

    except KeyboardInterrupt:
        print('Recording stopped.')
    finally:
        # Cleanup resources
        recorder.stop()
        koala.delete()

if __name__ == '__main__':
    noise_suppression()
