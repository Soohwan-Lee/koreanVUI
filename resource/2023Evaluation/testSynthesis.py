from openai import OpenAI
from pathlib import Path
import os
import soundfile as sf
import numpy as np
import time
from gtts import gTTS




# Create a folder to store the audio files
output_folder = "audio_files"
os.makedirs(output_folder, exist_ok=True)
file_path = "./resource/2023Evaluation/"

client = OpenAI(api_key="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")


# List of 30 strings
text_list = [
    "기분어때",
    "날씨 안내해줘",
    "내일",
    "날짜",
    "오늘",
    "오늘날씨",
    "거실 불 꺼",
    "거실 불 켜",
    "거실난방꺼",
    "지금 몇시니",
    "조명 어둡게",
    "큰 방",
    "현재시간",
    "티비켜",
    "보일러켜",
    "충전하러가",
    "오늘며칠이야",
    "안방 불 꺼라",
    "안방난방온도올려",
    "온도올려",
    "안방",
    "날씨정보",
    "토요일",
    "오늘 무슨요일이니",
    "안방 불 켜",
    "내일날씨",
    "침실 불 켜",
    "침실점등",
    "소리 줄여줘",
    "소리 크게"
]

# i = 10
# speech_file_path = Path(__file__).parent / f"{i}.mp3"    
# response = client.audio.speech.create(
# model="tts-1-hd",
# voice="shimmer",
# input=text_list[i]
# )

# response.stream_to_file(speech_file_path)

# audio_data,sample_rate = sf.read(speech_file_path)

# Loop through the 30 pieces of text
for i, text in enumerate(text_list):
    # # Convert text to speech
    tts = gTTS(text=text, lang='ko')
    tts.save("./resource/2023Evaluation/" + f"{i}.wav")

    # speech_file_path = Path(__file__).parent / f"{i}.mp3"    
    # response = client.audio.speech.create(
    # model="tts-1-hd",
    # voice="shimmer",
    # input=text
    # )

    # response.stream_to_file(speech_file_path)

    # audio_data,sample_rate = sf.read(speech_file_path)

print("Audio files created and saved successfully.")
