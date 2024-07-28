import requests
import pyaudio
import soundfile as sf
import io
import time

def streamed_audio(input_text, api_key, model='tts-1', voice='nova'):
    start_time = time.time()
    # OpenAI API endpoint and parameters
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f'Bearer {api_key}',  # Use the provided API key
    }

    data = {
        "model": model,
        "input": input_text,
        "voice": voice,
        "response_format": "opus",
    }

    audio = pyaudio.PyAudio()

    def get_pyaudio_format(subtype):
        if subtype == 'PCM_16':
            return pyaudio.paInt16
        return pyaudio.paInt16

    with requests.post(url, headers=headers, json=data, stream=True) as response:
        if response.status_code == 200:
            buffer = io.BytesIO()
            for chunk in response.iter_content(chunk_size=4096):
                buffer.write(chunk)
            
            buffer.seek(0)

            with sf.SoundFile(buffer, 'r') as sound_file:
                format = get_pyaudio_format(sound_file.subtype)
                channels = sound_file.channels
                rate = sound_file.samplerate

                stream = audio.open(format=format, channels=channels, rate=rate, output=True)
                chunk_size = 1024
                data = sound_file.read(chunk_size, dtype='int16')
                print(f"Time to play: {time.time() - start_time} seconds")

                while len(data) > 0:
                    stream.write(data.tobytes())
                    data = sound_file.read(chunk_size, dtype='int16')

                stream.stop_stream()
                stream.close()
        else:
            print(f"Error: {response.status_code} - {response.text}")

        audio.terminate()

        return f"Time to play: {time.time() - start_time} seconds"

if __name__ == "__main__":
    api_key = "YOUR_API_KEY"  # Enter your API key here // YOUR_API_KEY
    input_text = "Today is a wonderful day to build something people love!"
    streamed_audio(input_text, api_key)




# from pathlib import Path
# from openai import OpenAI

# # YOUR_API_KEY
# client = OpenAI(api_key="YOUR_API_KEY")

# speech_file_path = "./resource/speechSynthesis/english/speech.mp3"
# # response = "Today is a wonderful day to build something people love!"
# response = client.audio.speech.create(
#   model="tts-1",
#   voice="nova",
#   input="Today is a wonderful day to build something people love!"
# )

# response.stream_to_file(speech_file_path)