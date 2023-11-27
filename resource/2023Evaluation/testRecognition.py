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
# from tools import revise
import time  # 시간 측정을 위한 모듈 추가
import os
import librosa

file_path = "./resource/2023Evaluation/"

model_path = file_path + 'model.pt'
device = 'cpu'
model = torch.load(model_path, map_location=lambda storage, loc: storage).to(device)
vocab = KsponSpeechVocabulary(file_path + 'cssiri_character_vocabs.csv')
transforms = FilterBank(48000, 80, 20, 10)

# def resampling(input_wav, origin_sr, resample_sr):
#     y, sr = librosa.load(input_wav, sr=origin_sr)
#     resample = librosa.resample(y, sr, resample_sr)
#     return resample
#     # print("original wav sr: {}, original wav shape: {}, resample wav sr: {}, resmaple shape: {}".format(origin_sr, y.shape, resample_sr, resample.shape))


for i in range(30):
    signal = load_audio(file_path + f"{i}.wav", True, "wav")
    # signal = resampling(signal, 24000, 48000)

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

        sentence = vocab.label_to_string(y_hats.cpu().detach().numpy())[0]
        print(f"인식된 텍스트: {sentence}") 
    # print(f"환경: {device}\n모델 불러오기: {elapsed_time:.3f} 초\n음성 불러오기: {elapsed_time_2:.3f} 초\n예측: {elapsed_time_3:.3f} 초\n전체 소요시간: {entire_time:.3f} 초")
    # with wave.open(wav_file, 'rb') as wf:
    #     print(f"음성 길이: {wf.getnframes()/wf.getframerate()} 초, 음성 크기: {os.path.getsize(wav_file)/1000} kB\n")