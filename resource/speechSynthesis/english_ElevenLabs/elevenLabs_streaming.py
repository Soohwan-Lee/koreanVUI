import os
from typing import IO
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
from pydub.playback import play

# ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
    api_key="ELEVENLABS_API_KEY",
)

# Female Robot ID: weA4Q36twV5kwSaTEL0Qㄴ
# Foxy ID(Futuristic Robotic Personal AGI): 4y14Rc2ZMTzfnlc2o7X4

def text_to_speech_stream(text: str) -> IO[bytes]:
    # Perform the text-to-speech conversion
    response = client.text_to_speech.convert(
        voice_id="4y14Rc2ZMTzfnlc2o7X4", # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Create a BytesIO object to hold the audio data in memory
    audio_stream = BytesIO()

    # Write each chunk of audio data to the stream
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    # Reset stream position to the beginning
    audio_stream.seek(0)

    # Return the stream for further use
    return audio_stream

# Convert text to speech and get the audio stream
audio_stream = text_to_speech_stream("Hello! My Name is Lemmy! Nice to meet you! What can I help for you?")

# Load the audio stream into pydub's AudioSegment
audio = AudioSegment.from_file(audio_stream, format="mp3")

# Play the audio
play(audio)
