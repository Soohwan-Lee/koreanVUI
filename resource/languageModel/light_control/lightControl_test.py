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


# Arduino control
serial_port = '/dev/cu.usbserial-14120'  # Replace with your Arduino serial port
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

# speech Recognition
RATE = 44100
CHUNK = int(RATE / 10)
BUFF = CHUNK * 10
FORMAT = pyaudio.paInt16
CHANNELS = 1
DEVICE = 2

file_path = './resource/languageModel/'



client = OpenAI(
  api_key='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'  # this is also the default, it can be omitted
)

def turn_on_light (location):
    print(location + "의 불을 켭니다.")
    if location == '침실':
        data = '2'
        ser.write(data.encode())  # Convert string to bytes before sending
    elif location == '거실':
        data = '4'
        ser.write(data.encode())  # Convert string to bytes before sending
    elif location == '주방':
        data = '6'
        ser.write(data.encode())  # Convert string to bytes before sending


def turn_off_light (location):
    print(location + "의 불을 끕니다.")
    if location == '침실':
        data = '1'
        ser.write(data.encode())  # Convert string to bytes before sending
    elif location == '거실':
        data = '3'
        ser.write(data.encode())  # Convert string to bytes before sending
    elif location == '주방':
        data = '5'
        ser.write(data.encode())  # Convert string to bytes before sending

tools = [
  {
    "type": "function",
    "function": {
      "name": "turn_on_light",
      "description": "방 이름을 입력해서 그곳의 불 켜기",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "방 이름, 예를 들면 침실, 거실, 주방",
          },
        },
        "required": ["location"],
      },
    },
  },
    {
    "type": "function",
    "function": {
      "name": "turn_off_light",
      "description": "방 이름을 입력해서 그곳의 불 끄기",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "방 이름, 예를 들면 침실, 거실, 주방",
          },
        },
        "required": ["location"],
      },
    },
  }
]

def run_conversation(user_query):
    # 사용자 입력
    messages = [{"role": "user", "content": user_query}] 

    completion = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=messages,
    tools=tools,
    tool_choice="auto"
    )
    completion_reponse = completion.choices[0].message
    # print(completion_reponse)

    if completion_reponse.tool_calls: # 응답이 함수 호출인지 확인하기
        # 호출할 함수 이름을 지정 
        available_functions = {"turn_on_light": turn_on_light, "turn_off_light": turn_off_light}

        # 함수 이름 추출
        # print(completion_reponse)
        for tool_call in completion_reponse.tool_calls:
            # function_name = completion_reponse.tool_calls[0].function.name
            function_name = tool_call.function.name

            
            # 호출할 함수 선택
            fuction_to_call = available_functions[function_name]

            # 함수 호출 및 반환 결과 받기
            fuction_to_call(
                location=json.loads(tool_call.function.arguments).get('location')
            )
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

    audio_file = open("./resource/languageModel/realtime_input.wav", "rb")


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