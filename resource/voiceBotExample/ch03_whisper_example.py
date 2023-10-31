import openai
import pyaudio
import wave
import time
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000

file_path = './resource/voiceBotExample/'

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


### OpenAI STT
#API 키 입력
openai.api_key = "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"

start_time = time.time()  # 시간 측정 시작

# 녹음파일 열기
audio_file = open("./resource/voiceBotExample/realtime_input.wav", "rb")

start_time_2 = time.time()  # 시간 측정 시작

# whisper 모델에 음원파일 전달하기
transcript = openai.Audio.transcribe("whisper-1", audio_file)

start_time_3 = time.time()  # 시간 측정 시작

elapsed_time = start_time_2 - start_time
elapsed_time_2 = start_time_3 - start_time_2
entire_time = start_time_3 - start_time

#결과 보기
print("Whisper가 인식한 음성: " + transcript["text"])
print(f"음성 불러오기: {elapsed_time:.3f} 초\nWhisper 결과 불러오기: {elapsed_time_2:.3f} 초\n전체 소요시간: {entire_time:.3f} 초")
with wave.open(wav_file, 'rb') as wf:
    print(f"음성 길이: {wf.getnframes()/wf.getframerate()} 초, 음성 크기: {os.path.getsize(wav_file)/1000} kB\n")