import whisper

# Set the path to the WAV file
file_path = "./resource/speechRecognition/localWhisper/testSample.wav"  # Update this to your actual file path

# Load Whisper model (e.g., "tiny" for a smaller, faster model)
model = whisper.load_model("tiny")

def speech_to_text(file_path):
    # Transcribe the audio file to text
    result = model.transcribe(file_path, fp16=False)
    return result

if __name__ == '__main__':
    # Call the function and print the transcribed text
    result = speech_to_text(file_path)
    transcribed_text = result["text"]
    print(transcribed_text)
