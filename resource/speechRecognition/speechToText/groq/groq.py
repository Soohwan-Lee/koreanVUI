import time
from openai import OpenAI

def transcribe_audio():
    groq = OpenAI(api_key="YOUR_API_KEY", base_url="https://api.groq.com/openai/v1")
    audio_file = open("./resource/speechRecognition/speechToText/groq/testSample.wav", "rb")
    transcript = groq.audio.transcriptions.create(
        model="whisper-large-v3",
        file=audio_file,
        response_format="text"
    )
    return transcript

if __name__ == "__main__":
    # Start the timer
    start_time = time.time()

    # Perform the transcription
    transcript = transcribe_audio()
    print(transcript)

    # End the timer
    end_time = time.time()

    # Calculate and print the execution time
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")

# from openai import OpenAI
# groq = OpenAI (api_key="YOUR_API_KEY" , base_url="https://api.groq.com/openai/v1")
# audio_file = open("./resource/speechRecognition/speechToText/groq/testSample.wav", "rb")
# transcript = groq.audio.transcriptions.create(
#     model="whisper-large-v3",
#     file=audio_file,
#     response_format="text"
# )
# print(transcript)