from openai import OpenAI
from pathlib import Path

import sounddevice as sd
import soundfile as sf
import yaml
import pyaudio
import numpy as np
from array import array
from collections import deque
from queue import Queue, Full
from threading import Thread
import wave
import kospeech.data.audio.core as core

import torch
import torch.nn as nn
from kospeech.vocabs.ksponspeech import KsponSpeechVocabulary
from kospeech.models import DeepSpeech2
from kospeech.data.audio.feature import FilterBank
from kospeech.data.audio.parser import load_audio
import time  # 시간 측정을 위한 모듈 추가

RATE = 44100
CHUNK = int(RATE / 10)
BUFF = CHUNK * 10
FORMAT = pyaudio.paInt16
CHANNELS = 1
DEVICE = 1

# 무음 감지를 위한 상수 값
SILENCE_THREASHOLD = 2500
SILENCE_SECONDS = 2

# 파일 경로 설정
file_path = './resource/merge/'

client = OpenAI(api_key="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")
personality = "너는 노인들을 위한 친절한 반려 로봇이야. 공손히 대답해줘."
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
    print(response.choices[0].message.content)

    bot_response = response.choices[0].message.content
    messages.append({"role" : "assistant", "content" : f"{bot_response}"})
    return bot_response

# 음성 인식 모델을 사용하는 함수 (주석 처리)
def speech_recognition(signal):
    #print(signal)

    start = time.time() # 시간 측정

    model_path = file_path + 'model.pt'
    device = 'cpu' # 'cuda'
    model = torch.load(model_path, map_location=lambda storage, loc: storage).to(device)
    vocab = KsponSpeechVocabulary(file_path + 'cssiri_character_vocabs.csv')
    transforms = FilterBank(48000, 80, 20, 10)

    time1 = time.time() # 시간 측정

    feature = transforms(torch.FloatTensor(signal))
    feature -= feature.mean()
    feature /= np.std(feature)
    feature = torch.FloatTensor(feature).transpose(0, 1).to(device)
    input_length = torch.LongTensor([len(feature)]).to(device)

    if isinstance(model, nn.DataParallel):
        model = model.module
    model.eval()

    if isinstance(model, DeepSpeech2):
        y_hats = model.recognize(feature.unsqueeze(0), input_length)
        time2 = time.time() # 시간 측정
        sentence = vocab.label_to_string(y_hats.cpu().detach().numpy())[0]
        end = time.time() # 시간 측정
        print(f"\n인식된 텍스트: {sentence}") 
        print(f"환경: {device}\n모델 불러오기: {time1-start:.3f} 초\n음성 인식: {time2-time1:.3f} 초\n후처리: {end-time2:.3f} 초")
        print("===========================================")
        return sentence



def save_audio_data(data, filename):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

def listen(q):
    audio = pyaudio.PyAudio()
    print("===========================================")
    for index in range(audio.get_device_count()):
        desc = audio.get_device_info_by_index(index)
        print("DEVICE: {device}, INDEX: {index}, RATE: {rate} ".format(
            device=desc["name"], index=index, rate=int(desc["defaultSampleRate"])))
    print("===========================================")
    is_started = False
    vol_que = deque(maxlen=SILENCE_SECONDS)
    signal_data = []

    # 스레딩을 위한 수신 기능 정의
    while True:
        # open stream
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=DEVICE,
            frames_per_buffer=CHUNK
        )

        # FIXME: 초기 잡음 데이터 내보내기(1초)
        for _ in range(0, int(RATE / CHUNK)):
            data = stream.read(CHUNK, exception_on_overflow=False)


        print('start listening')
        while True:
            try:
                # 1초 동안 볼륨 합계를 저장하는 임시 변수를 정의
                vol_sum = 0

                # 1초 동안 청크 단위로 데이터 읽기
                for _ in range(0, int(RATE / CHUNK)):
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    
                    # 청크 데이터의 최대 볼륨을 가져오고, 볼륨 합계를 업데이트
                    vol = max(array('h', data))
                    vol_sum += vol

                    # 상태가 수신 중이면 볼륨 값을 확인
                    if not is_started:
                        if vol >= SILENCE_THREASHOLD:
                            print('** start of speech detected')
                            is_started = True

                    # 상태가 음성 시작인 경우, 데이터 쓰기
                    if is_started:
                        q.put(data)
                        signal_data.append(data)

                # 상태가 음성 시작인 경우, 볼륨 대기열을 업데이트하고 무음을 확인
                if is_started:
                    vol_que.append(vol_sum / (RATE / CHUNK) < SILENCE_THREASHOLD)
                    if len(vol_que) == SILENCE_SECONDS and all(vol_que):
                        print('** end of speech detected')

                        # 음성 감지가 종료되면 큐에 저장된 데이터를 음성 인식 코드로 전달
                        #while not q.empty():
                        if signal_data:
                            byte_data = b''.join(signal_data)

                            signal = np.frombuffer(byte_data, dtype='h').astype('float32')
                            non_silence_indices = core.split(signal, top_db=30)
                            signal = np.concatenate([signal[start:end] for start, end in non_silence_indices])
                            signal = signal / 32767

                            speech_recognition(signal)  # 이 부분에서 데이터를 출력

                            # 일정 시간 동안 대기
                            time.sleep(1)

                        is_started = False
                        vol_que.clear()
                        signal_data = []
                        break
            except Full:
                pass

        # 스트림 닫기
        stream.stop_stream()
        stream.close()


def main():
    while True:
        q = Queue()
        user_input = Thread(target=listen, args=(q,)).start()
        messages.append({"role" : "user", "content" : f"{user_input}"})
        bot_response = generate_text()
        generate_audio(bot_response)

if __name__ == "__main__":
    main()