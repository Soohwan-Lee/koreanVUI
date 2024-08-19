from pathlib import Path
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_API_KEY")

# List of voice actors
voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

# Input text to be converted to speech
input_text = "Hello! My Name is Lemmy! Nice to Meet you!"

# Directory to save the speech files
output_dir = Path("./resource/speechSynthesis/english/")
output_dir.mkdir(parents=True, exist_ok=True)

# Generate speech for each voice and save to file
for voice in voices:
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=input_text
    )
    
    # File path for the current voice
    speech_file_path = output_dir / f"{voice}_speech.mp3"
    
    # Save the speech to file
    response.stream_to_file(str(speech_file_path))

print("Speech synthesis completed for all voices.")
