import sounddevice as sd
import urllib.request
import soundfile as sf


file_path = "./resource/speechSynthesis/responseSample/"

# Clova Voice API Information
client_id = "ut5pwvjdyo"
client_secret = "uqvEbZ2kasYTH8LVWTtyqC53QeyDa8R4kENLBaBu"

def generate_audio(text):
    encText = urllib.parse.quote(text)

    ### Set Parameter
    speaker = "vdain"
    volume = "VOLUME"       # -5 ~ +5 / -5:0.5배 낮은 볼륨, +5: 1.5배 큰 볼륨
    speed = "SPEED"     # -5 ~ +5 / -5: 2배 빠른 속도, +5: 0.5배 느린 속도
    pitch = "PITCH"     # -5 ~ +5 / -5: 1.2배 높은 피치, +5: 0.8배 낮은 피치
    emotion = "0"     # 0:중립, 1: 슬픔, 2: 기쁨, 3: 분노
    emotion_strength = "EMOTION_STRENGTH"       # 0: 약함, 1: 보통, 2: 강함

    # speech_file_path = Path(__file__).parent / "clovaTemp.mp3"



    data = "speaker=" + speaker + "&volume=0&speed=0&pitch=0&format=mp3&emotion=" + emotion + "&emotion_strength=2&text=" + encText
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if(rescode==200):
        # print("TTS mp3 저장")
        response_body = response.read()
        with open(file_path + 'clovaTemp.mp3', 'wb') as f:
            f.write(response_body)
        # audio_data,sample_rate = sf.read(file_path + 'clovaTemp.mp3')
        # sd.play(audio_data,sample_rate)
        # sd.wait()
    else:
        print("Error Code(Clova Voice):" + rescode)

def main():
    print("This is main fuction!")
    text_sample = "안녕하세요."
    generate_audio(text_sample)

if __name__ == "__main__":
    main()