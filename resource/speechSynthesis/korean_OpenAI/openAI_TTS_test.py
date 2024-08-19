from pathlib import Path
from openai import OpenAI
import yaml
import sounddevice as sd
import soundfile as sf
import numpy as np

# with open("keys.yaml", "r") as file:
#     keys = yaml.safe_load(file)

client = OpenAI(api_key="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")

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1-hd",
  voice="shimmer",
  input="안녕하세요! 저는 당신을 도와주는 친절한 로봇 래미 입니다!"
)

response.stream_to_file(speech_file_path)

audio_data,sample_rate = sf.read(speech_file_path)
sd.play(audio_data,sample_rate)
sd.wait()