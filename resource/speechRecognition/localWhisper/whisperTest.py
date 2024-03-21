import whisper
import pyaudio
import wave


# const values for mic streaming
# RATE = 48000
RATE = 44100
CHUNK = int(RATE / 10)
BUFF = CHUNK * 10
FORMAT = pyaudio.paInt16
CHANNELS = 1
DEVICE = 1

# 무음 감지를 위한 상수 값
SILENCE_THREASHOLD = 4000
SILENCE_SECONDS = 2

# Set File Path
file_path = "./resource/speechRecognition/localWhisper/"

# Load Whisper model (TINY)
model = whisper.load_model("tiny")

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

    # wav_file = file_path + "realtime_input.wav"

    # audio_file = open(file_path + "realtime_input.wav", "rb")


    # whisper 모델에 음원파일 전달하기
    # transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    # print("User: " + transcript.text)
    result = model.transcribe(file_path + "realtime_input.wav", fp16=False)
    # print(result)
    print(f'Text: {result["text"]}')
    # return transcript.text

def main():
    while True:
        print("========================")
        speech_recognition()

if __name__ == '__main__':
    main()


result = model.transcribe(file_path + "realtime_input.wav", fp16=False)
print(result)
print(f'Text: {result["text"]}')