import pyaudio
import numpy as np
import torch
import torch.nn as nn
import wave
import os
import google.cloud.dialogflow_v2 as dialogflow
from kospeech.vocabs.ksponspeech import KsponSpeechVocabulary
from kospeech.models import DeepSpeech2
from kospeech.data.audio.feature import FilterBank
from kospeech.data.audio.parser import load_audio
from tools import revise
import time  # 시간 측정을 위한 모듈 추가
import os

file_path = './resource/merge/'

### Audio Sample Rate
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000

### Google Dialog Flow
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = file_path + 'lemme2-hvvh-93b9c4459fd3.json'   #Private Key
DIALOGFLOW_PROJECT_ID = 'lemme2-hvvh'   #Project ID
DIALOGFLOW_LANGUAGE_CODE = 'ko'
SESSION_ID = 'me'
session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)




while True:
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print('\n=========================\n')
    print('Talk to Lemmy! (start recording)')

    frames = []
    seconds = 5 # 녹음 시간
    for i in range(0,int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    print("Wait Lemmy's Response! (record stopped)")

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
        start_time_4 = time.time()  # 시간 측정 시작
        sentence = vocab.label_to_string(y_hats.cpu().detach().numpy())[0]
    
    our_input = dialogflow.types.TextInput(text=sentence, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query = dialogflow.types.QueryInput(text=our_input)
    response = session_client.detect_intent(session=session, query_input=query)


    end_time = time.time()  # 시간 측정 종료
    elapsed_time = start_time_2 - start_time
    elapsed_time_2 = start_time_3 - start_time_2
    elapsed_time_3 = start_time_4 - start_time_3
    elapsed_time_4 = end_time - start_time_4
    entire_time = end_time - start_time

    print("\n----래미와 대화----")
    print(f"음성 인식된 텍스트: {sentence}")
    print("Lemmy's response:", response.query_result.fulfillment_text)
    print("Dialogflow's intent:", response.query_result.intent.display_name)
    print("\n----소요 시간 측정----")
    print(f"환경: {device}\n모델 불러오기: {elapsed_time:.3f} 초\n음성 불러오기: {elapsed_time_2:.3f} 초\n예측: {elapsed_time_3:.3f} 초\n다이얼로그플로우 불러오기: {elapsed_time_4:.3f}\n전체 소요시간: {entire_time:.3f} 초")
    with wave.open(wav_file, 'rb') as wf:
        print(f"음성 길이: {wf.getnframes()/wf.getframerate()} 초, 음성 크기: {os.path.getsize(wav_file)/1000} kB")