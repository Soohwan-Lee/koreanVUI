import whisper
import time

# Set the path to the WAV file
file_path = "./resource/speechRecognition/speechToText/localWhisper/testSample.wav"  # Update this to your actual file path

# Load Whisper model (e.g., "tiny" for a smaller, faster model)
model = whisper.load_model("base")

def speech_to_text(file_path):
    # Transcribe the audio file to text
    result = model.transcribe(file_path, fp16=False)
    return result

if __name__ == '__main__':
    # Start the timer
    start_time = time.time()

    # Call the function and print the transcribed text
    result = speech_to_text(file_path)
    transcribed_text = result["text"]
    print(transcribed_text)

    # End the timer
    end_time = time.time()

    # Calculate and print the execution time
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")

# import whisper

# # Set the path to the WAV file
# file_path = "./resource/speechRecognition/localWhisper/testSample.wav"  # Update this to your actual file path

# # Load Whisper model (e.g., "tiny" for a smaller, faster model)
# model = whisper.load_model("tiny")

# def speech_to_text(file_path):
#     # Transcribe the audio file to text
#     result = model.transcribe(file_path, fp16=False)
#     return result

# if __name__ == '__main__':
#     # Call the function and print the transcribed text
#     result = speech_to_text(file_path)
#     transcribed_text = result["text"]
#     print(transcribed_text)
