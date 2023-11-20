from openai import OpenAI
from pathlib import Path

import sounddevice as sd
import soundfile as sf
import pyaudio
import wave

RATE = 44100
CHUNK = int(RATE / 10)
BUFF = CHUNK * 10
FORMAT = pyaudio.paInt16
CHANNELS = 1
DEVICE = 1

file_path = './resource/merge/'



client = OpenAI(api_key="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")
personality = "너는 노인들을 위한 반려로봇 래미야. 질문에는 항상 친절하고 공손하게 대답해야 해"
messages = [{"role" : "system", "content" : f"{personality}"}]

def generate_audio(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=text
    )
    response.stream_to_file(speech_file_path)
    audio_data,sample_rate = sf.read(speech_file_path)
    sd.play(audio_data,sample_rate)
    sd.wait()

def generate_text():
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    print("LEMMY: "+ response.choices[0].message.content)

    bot_response = response.choices[0].message.content
    messages.append({"role" : "assistant", "content" : f"{bot_response}"})
    return bot_response

def speech_recognition():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=DEVICE,
                frames_per_buffer=CHUNK)

    print('start recording')

    frames = []
    seconds = 5 # 녹음 시간
    for i in range(0,int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    print('record stopped')

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(file_path + "realtime_input.wav",'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    wav_file = file_path + "realtime_input.wav"

    audio_file = open("./resource/merge/realtime_input.wav", "rb")


    # whisper 모델에 음원파일 전달하기
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    print("User: "+transcript.text)
    return transcript.text

def main():
    while True:
        user_input = speech_recognition()
        messages.append({"role" : "user", "content" : f"{user_input}"})
        bot_response = generate_text()
        generate_audio(bot_response)

if __name__ == "__main__":
    main()