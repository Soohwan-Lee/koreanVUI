import pyaudio
import numpy as np
import torch
import torch.nn as nn
import wave
import torchaudio
from kospeech.vocabs.ksponspeech import KsponSpeechVocabulary
from kospeech.models import DeepSpeech2
from kospeech.data.audio.feature import FilterBank
from kospeech.data.audio.parser import load_audio
from tools import revise
import time  # 시간 측정을 위한 모듈 추가
import os


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000

file_path = './resource/speechRecognition/demo_share/'

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
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

start_time = time.time()  # 시간 측정 시작

model_path = file_path + 'model.pt'
device = 'cpu'
model = torch.load(model_path, map_location=lambda storage, loc: storage).to(device)
vocab = KsponSpeechVocabulary(file_path + 'cssiri_character_vocabs.csv')
transforms = FilterBank(48000, 80, 20, 10)

start_time_2 = time.time()  # 시간 측정 시작

signal = load_audio(wav_file, True, "wav")

start_time_3 = time.time()  # 시간 측정 시작

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
    end_time = time.time()  # 시간 측정 종료
    elapsed_time = start_time_2 - start_time
    elapsed_time_2 = start_time_3 - start_time_2
    elapsed_time_3 = end_time - start_time_3
    entire_time = end_time - start_time

    sentence = vocab.label_to_string(y_hats.cpu().detach().numpy())[0]
    print(f"인식된 텍스트: {sentence}") 
    print(f"환경: {device}\n모델 불러오기: {elapsed_time:.3f} 초\n음성 불러오기: {elapsed_time_2:.3f} 초\n예측: {elapsed_time_3:.3f} 초\n전체 소요시간: {entire_time:.3f} 초")
    with wave.open(wav_file, 'rb') as wf:
        print(f"음성 길이: {wf.getnframes()/wf.getframerate()} 초, 음성 크기: {os.path.getsize(wav_file)/1000} kB\n")