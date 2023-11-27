# 네이버 음성합성 Open API 예제
import os
import sys
import urllib.request

file_path = "./resource/speechSynthesis/"

client_id = "72n60cfo9f"
client_secret = "dzkXmF4LioFti5YWa59Mogp0DUDRkNg7DBZ5mBEO"
encText = urllib.parse.quote("안녕하세요. 제 이름은 래미 입니다.")

### Set Parameter
speaker = "vyuna"
volume = "VOLUME"       # -5 ~ +5 / -5:0.5배 낮은 볼륨, +5: 1.5배 큰 볼륨
speed = "SPEED"     # -5 ~ +5 / -5: 2배 빠른 속도, +5: 0.5배 느린 속도
pitch = "PITCH"     # -5 ~ +5 / -5: 1.2배 높은 피치, +5: 0.8배 낮은 피치
emotion = "3"     # 0:중립, 1: 슬픔, 2: 기쁨, 3: 분노
emotion_strength = "EMOTION_STRENGTH"       # 0: 약함, 1: 보통, 2: 강함


data = "speaker=" + speaker + "&volume=0&speed=0&pitch=0&format=mp3&emotion=" + emotion + "&emotion_strength=2&text=" + encText
url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
request = urllib.request.Request(url)
request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
request.add_header("X-NCP-APIGW-API-KEY",client_secret)
response = urllib.request.urlopen(request, data=data.encode('utf-8'))
rescode = response.getcode()
if(rescode==200):
    print("TTS mp3 저장")
    response_body = response.read()
    with open(file_path + speaker + emotion + '.mp3', 'wb') as f:
        f.write(response_body)
else:
    print("Error Code:" + rescode)