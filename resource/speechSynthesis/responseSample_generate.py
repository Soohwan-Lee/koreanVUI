import sounddevice as sd
import urllib.request
import soundfile as sf
import urllib.parse

file_path = "./resource/speechSynthesis/responseSample/"

# Clova Voice API Information
client_id = "ut5pwvjdyo"
client_secret = "uqvEbZ2kasYTH8LVWTtyqC53QeyDa8R4kENLBaBu"

def generate_audio(text, file_name):
    encText = urllib.parse.quote(text)

    # Set Parameter
    speaker = "vdain"
    volume = 0      # 볼륨 설정 (-5 ~ +5)
    speed = 0       # 속도 설정 (-5 ~ +5)
    pitch = 0       # 피치 설정 (-5 ~ +5)
    emotion = "0"   # 감정 설정 (0:중립, 1: 슬픔, 2: 기쁨, 3: 분노)
    emotion_strength = 2  # 감정 강도 설정 (0: 약함, 1: 보통, 2: 강함)

    data = f"speaker={speaker}&volume={volume}&speed={speed}&pitch={pitch}&format=mp3&emotion={emotion}&emotion_strength={emotion_strength}&text={encText}"
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        with open(file_path + file_name, 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code(Clova Voice): " + str(rescode))

def main():
    response_samples = [
        ("1_1.mp3", "네, 알겠습니다."),
        ("1_2.mp3", "명령을 수행하겠습니다."),
        ("1_3.mp3", "지금 바로 처리할게요."),
        ("1_4.mp3", "주문하신대로 진행하겠습니다."),
        ("1_5.mp3", "이제 시작하겠습니다."),
        ("1_6.mp3", "알겠습니다, 즉시 처리해드릴게요."),
        ("2_1.mp3", "알겠어요, 바로 도와드릴게요."),
        ("2_2.mp3", "당신의 요청을 기쁜 마음으로 수행할게요."),
        ("2_3.mp3", "언제든지 도와드리겠습니다!"),
        ("2_4.mp3", "항상 여기 있어서 도움을 드릴 수 있어 기뻐요."),
        ("2_5.mp3", "당신의 명령을 듣고 바로 행동하겠습니다, 안심하세요."),
        ("2_6.mp3", "저에게 맡겨주셔서 감사합니다, 즐겁게 수행할게요."),
        ("3_1.mp3", "이것을 지금 실행해도 괜찮을까요?"),
        ("3_2.mp3", "무엇을 더 도와드릴까요?"),
        ("3_3.mp3", "해당 작업을 시작하기 전에 더 확인해야 할 사항이 있나요?"),
        ("3_4.mp3", "조금 더 구체적으로 말씀해 주실 수 있나요?"),
        ("3_5.mp3", "이 작업을 우선순위로 두어도 될까요?"),
        ("3_6.mp3", "추가로 준비해야 할 사항이 있을까요?"),
        ("4_1.mp3", "뿅! 바로 처리하겠습니다."),
        ("4_2.mp3", "딩동! 모든 준비가 완료되었어요."),
        ("4_3.mp3", "총총총, 바로 그렇게 해드릴게요."),
        ("4_4.mp3", "쓰윽! 바로 처리하겠습니다."),
        ("4_5.mp3", "투두둑! 모든 설정을 완료했습니다."),
        ("4_6.mp3", "와글와글! 이제부터 저와 함께할 시간이에요."),
        ("5_1.mp3", "요청을 시작합니다. 잠시만 기다려 주세요."),
        ("5_2.mp3", "지금 준비 중입니다. 곧 해결해드릴게요"),
        ("5_3.mp3", "지금부터 시작할게요, 편안하게 계세요."),
        ("5_4.mp3", "이제 절반 정도 끝났습니다. 조금만 더 기다려 주세요."),
        ("5_5.mp3", "모든 것이 순조롭게 진행되고 있어요."),
        ("5_6.mp3", "조금 더 시간이 걸릴 것 같아요. 안심하고 기다려 주세요."),
        ("6_1.mp3", "이제 저와 함께라면 지루할 틈이 없겠죠!"),
        ("6_2.mp3", "또 무엇을 도와드릴까요, 오늘은 제가 종일 바쁘답니다!"),
        ("6_3.mp3", "걱정 마세요, 제가 여기 있잖아요!"),
        ("6_4.mp3", "제가 로봇이지만, 때때로 나름대로 재미있답니다!"),
        ("6_5.mp3", "오늘도 활기찬 하루를 시작해 볼까요?"),
        ("6_6.mp3", "저도 이 일을 할 준비가 되어 있어요, 우리 함께 해요!")
    ]

    for file_name, text in response_samples:
        generate_audio(text, file_name)

if __name__ == "__main__":
    main()
