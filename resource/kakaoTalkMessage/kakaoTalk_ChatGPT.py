import requests
import os
import json
import re
# import openai
import os
import time
from openai import OpenAI
import serial
from pathlib import Path

import sounddevice as sd
import soundfile as sf
import pyaudio
import wave

from yeelight import Bulb



# # Arduino control
# serial_port = '/dev/cu.usbserial-14120'  # Replace with your Arduino serial port
# baud_rate = 9600
# ser = serial.Serial(serial_port, baud_rate)

# 카카오 API 엑세스 토큰
with open("./resource/kakaoTalkMessage/kakao_code_friend.json", "r") as fp:
    tokens = json.load(fp)    
print(tokens["access_token"])


# 친구 목록 가져오기
url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 목록 가져오기
header = {"Authorization": 'Bearer ' + tokens["access_token"]}
result = json.loads(requests.get(url, headers=header).text)
friends_list = result.get("elements")
print(friends_list)

# 친구 목록 중 0번째 리스트의 친구 'uuid'
friend_id = friends_list[0].get("uuid")
print(friend_id)

# 카카오톡 메시지 보내기
def send_message():
    url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    header = {"Authorization": 'Bearer ' + tokens["access_token"]}
    data={
        'receiver_uuids': '["{}"]'.format(friend_id),
        "template_object": json.dumps({
            "object_type":"text",
            "text":"[LEMMY Test] 응급상황 발생!",
            "link":{
                "web_url" : "https://expc.unist.ac.kr",
                "mobile_web_url" : "https://expc.unist.ac.kr"
            },
            "button_title": "119 호출하기"
        })
    }
    response = requests.post(url, headers=header, data=data)
    response.status_code

# speech Recognition
RATE = 44100
CHUNK = int(RATE / 10)
BUFF = CHUNK * 10
FORMAT = pyaudio.paInt16
CHANNELS = 1
DEVICE = 0

# Set File Path
file_path = './resource/kakaoTalkMessage/'


# # Function set color of light
# def setRGB_light(location, r,g,b):
#     if location == "거실":
#         placeBulb = livingRoomBulb
#     elif location == "침실":
#         placeBulb = bedRoomBulb

#     placeBulb.set_rgb(int(r),int(g),int(b))


client = OpenAI(
  api_key='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'  # this is also the default, it can be omitted
)

tools = [
  {
    "type": "function",
    "function": {
      "name": "send_message",
      "description": "응급 상황이라고 판단될 경우, 메시지를 보내기",
      "parameters": {
        # "type": "object",
        # "properties": {
        #   "location": {
        #     "type": "string",
        #     "description": "방 이름, 예를 들면 침실, 거실",
        #   },
        # },
        # "required": ["location"],
      },
    },
  }
  
    # {
  #   "type": "function",
  #   "function": {
  #     "name": "setRGB_light",
  #     "description": "방 이름과 색 이름을 r,g,b 형태로 입력해서 그곳의 색상 바꾸기",
  #     "parameters": {
  #       "type": "object",
  #       "properties": {
  #         "location": {
  #           "type": "string",
  #           "description": "방 이름, 예를 들면 침실, 거실",
  #         },
  #         "r": {
  #           "type": "int",
  #           "description": "색의 r 값, 예를 들면, 빨간색이면 255",
  #         },
  #         "g": {
  #           "type": "string",
  #           "description": "색의 g 값, 예를 들면, 빨간색이면 0",
  #         },
  #         "b": {
  #           "type": "string",
  #           "description": "색의 b 값, 예를 들면, 빨간색이면 0",
  #         },
  #       },
  #       "required": ["location", "r", "g", "b"],
  #     },
  #   },
  # }
]

def run_conversation(user_query):
    # 사용자 입력
    messages = [{"role": "user", "content": user_query}] 

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    tools=tools,
    tool_choice="auto"
    )
    completion_reponse = completion.choices[0].message
    # print(completion_reponse)

    if completion_reponse.tool_calls: # 응답이 함수 호출인지 확인하기
        # 호출할 함수 이름을 지정 
        available_functions = {"send_message": send_message}

        # 함수 이름 추출
        # print(completion_reponse)
        for tool_call in completion_reponse.tool_calls:
            # function_name = completion_reponse.tool_calls[0].function.name
            function_name = tool_call.function.name

            
            # 호출할 함수 선택
            function_to_call = available_functions[function_name]

            # 함수 호출 및 반환 결과 받기
            function_to_call()
            # function_to_call(
            #     location=json.loads(tool_call.function.arguments).get('location')
            # )
        # print(completion_reponse.tool_calls[0].function.name)

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

    audio_file = open("./resource/controlIoT/realtime_input.wav", "rb")


    # whisper 모델에 음원파일 전달하기
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    print("User: "+ transcript.text)
    return transcript.text

    
def main():
    while True:
        user_query = speech_recognition()
        run_conversation(user_query)
    # response_content = response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    main()