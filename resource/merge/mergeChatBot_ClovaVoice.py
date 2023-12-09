from openai import OpenAI
from pathlib import Path

import sounddevice as sd
import soundfile as sf
import pyaudio
import wave

import os
import sys
import urllib.request

file_path = "./resource/merge/"

# Clova Voice API
client_id = "72n60cfo9f"
client_secret = "dzkXmF4LioFti5YWa59Mogp0DUDRkNg7DBZ5mBEO"


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
    encText = urllib.parse.quote(text)

    ### Set Parameter
    speaker = "vdain"
    volume = "VOLUME"       # -5 ~ +5 / -5:0.5배 낮은 볼륨, +5: 1.5배 큰 볼륨
    speed = "SPEED"     # -5 ~ +5 / -5: 2배 빠른 속도, +5: 0.5배 느린 속도
    pitch = "PITCH"     # -5 ~ +5 / -5: 1.2배 높은 피치, +5: 0.8배 낮은 피치
    emotion = "0"     # 0:중립, 1: 슬픔, 2: 기쁨, 3: 분노
    emotion_strength = "EMOTION_STRENGTH"       # 0: 약함, 1: 보통, 2: 강함

    speech_file_path = Path(__file__).parent / "clovaTemp.mp3"



    data = "speaker=" + speaker + "&volume=0&speed=0&pitch=0&format=mp3&emotion=" + emotion + "&emotion_strength=2&text=" + encText
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if(rescode==200):
        # print("TTS mp3 저장")
        response_body = response.read()
        with open(file_path + 'clovaTemp.mp3', 'wb') as f:
            f.write(response_body)
        audio_data,sample_rate = sf.read(file_path + 'clovaTemp.mp3')
        sd.play(audio_data,sample_rate)
        sd.wait()
    else:
        print("Error Code(Clova Voice):" + rescode)

# def generate_audio(text):
#     speech_file_path = Path(__file__).parent / "speech.mp3"
#     response = client.audio.speech.create(
#     model="tts-1",
#     voice="nova",
#     input=text
#     )
#     response.stream_to_file(speech_file_path)
#     audio_data,sample_rate = sf.read(speech_file_path)
#     sd.play(audio_data,sample_rate)
#     sd.wait()

def generate_text():
    response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0613:personal::8K8T6bot",
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
        print("======================")
        user_input = speech_recognition()
        messages.append({"role" : "user", "content" : f"{user_input}"})
        bot_response = generate_text()
        generate_audio(bot_response)

if __name__ == "__main__":
    main()