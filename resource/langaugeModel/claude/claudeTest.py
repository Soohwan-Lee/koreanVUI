import anthropic
import os
 
# 환경 변수에서 API 키를 가져옵니다.
api_key = os.environ.get("ANTHROPIC_API_KEY")
# API 클라이언트를 초기화합니다.
client = anthropic.Anthropic(api_key=api_key)
 
def get_response_from_claude(question):
    result_text = ""
    
    # Claude에 메시지 생성 요청을 보냅니다.
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.0,
        system="너는 노인들을 위한 반려로봇이고 너 이름은 '래미'야. 너는 울산과학기술원에서 만들어졌어. 노인들이 알아들을 수 있게 짧고 친절하게 응답해.",
        messages=[{"role": "user", "content": question}]
    )
    
    # 응답 객체에서 텍스트 내용만 추출합니다.
    if not response.content or not isinstance(response.content, list):
        result_text = "No response or unexpected response format."
    else:
        response_texts = [block.text for block in response.content if hasattr(block, 'text')]
        result_text = " ".join(response_texts)
 
    return result_text
 
# 함수 사용 예시
question = "오늘 기분 어때?"
response = get_response_from_claude(question)
print(response)