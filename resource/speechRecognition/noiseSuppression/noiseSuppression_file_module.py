import struct
import wave
from pvkoala import create

def noise_suppression():
    # Hardcoded values for demonstration
    access_key = '9x0FaA466xUKn2jZkaAgAakVVBOG7RV6CFf/jI7rCpHJ3NB0HJ3V1w=='
    input_path = './resource/speechRecognition/noiseSuppression/testSample.wav'
    output_path = './resource/speechRecognition/noiseSuppression/testSample_withoutNoise.wav'

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

if __name__ == '__main__':
    noise_suppression()
