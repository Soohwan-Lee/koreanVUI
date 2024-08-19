import pyaudio
import soundfile as sf
import io
import time
from openai import OpenAI

def streamed_audio(input_text, api_key, model='tts-1', voice='nova'):
    start_time = time.time()
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    audio = pyaudio.PyAudio()

    def get_pyaudio_format(subtype):
        if subtype == 'PCM_16':
            return pyaudio.paInt16
        return pyaudio.paInt16

    # Create speech using OpenAI client
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=input_text,
        response_format="opus"
    )

    # Stream the audio data
    buffer = io.BytesIO(response.content)
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

    audio.terminate()
    return f"Time to play: {time.time() - start_time} seconds"

if __name__ == "__main__":
    api_key = "YOUR_API_KEY"  # Replace with your actual API key // YOUR_API_KEY
    input_text = "Hi there! My name is Lemmy! How can I help you today?"
    streamed_audio(input_text, api_key)

# import pyaudio
# import soundfile as sf
# import io
# import time
# from openai import OpenAI

# def streamed_audio(input_text, api_key, model='tts-1', voice='nova'):
#     start_time = time.time()

#     # Initialize OpenAI client
#     client = OpenAI(api_key=api_key)

#     # Generate speech using OpenAI API
#     response = client.audio.speech.create(
#         model=model,
#         voice=voice,
#         input=input_text
#     )

#     # Access binary content from the response
#     audio_data = response.content  # Assuming the audio data is in the content attribute

#     # Streaming audio setup
#     audio = pyaudio.PyAudio()

#     def get_pyaudio_format(subtype):
#         if subtype == 'PCM_16':
#             return pyaudio.paInt16
#         return pyaudio.paInt16

#     buffer = io.BytesIO(audio_data)
#     buffer.seek(0)

#     with sf.SoundFile(buffer, 'r') as sound_file:
#         format = get_pyaudio_format(sound_file.subtype)
#         channels = sound_file.channels
#         rate = sound_file.samplerate

#         stream = audio.open(format=format, channels=channels, rate=rate, output=True)
#         chunk_size = 1024
#         data = sound_file.read(chunk_size, dtype='int16')
#         print(f"Time to play: {time.time() - start_time} seconds")

#         while len(data) > 0:
#             stream.write(data.tobytes())
#             data = sound_file.read(chunk_size, dtype='int16')

#         stream.stop_stream()
#         stream.close()

#     audio.terminate()

#     return f"Time to play: {time.time() - start_time} seconds"

# if __name__ == "__main__":
#     api_key = "YOUR_API_KEY"  # Enter your API key here
#     input_text = "Today is a wonderful day to build something people love!"
#     print(streamed_audio(input_text, api_key))
