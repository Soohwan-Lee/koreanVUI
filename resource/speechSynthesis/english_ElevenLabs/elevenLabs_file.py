
import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

# ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
    api_key="YOUR_API_KEY",
)

# Female Robot ID: weA4Q36twV5kwSaTEL0Q
# Foxy ID(Futuristic Robotic Personal AGI): 4y14Rc2ZMTzfnlc2o7X4

def text_to_speech_file(text: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="4y14Rc2ZMTzfnlc2o7X4", # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5", # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # uncomment the line below to play the audio back
    # play(response)

    # Generating a unique file name for the output MP3 file
    # save_file_path = f"{uuid.uuid4()}.mp3"
    save_file_path = "./resource/speechSynthesis/english_ElevenLabs/foxy.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path

text_to_speech_file("Hello! My Name is Lemmy! Nice to meet you! What can I help for you?")
