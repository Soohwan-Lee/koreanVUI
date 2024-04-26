import anthropic

### Posible Models
# claude-3-haiku-20240307
# claude-3-sonnet-20240229
# claude-3-opus-20240229

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="YOUR-API-KEY",
)
message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    temperature=0,
    system="너는 노인들을 위한 반려로봇이고 너 이름은 '래미'야. 너는 울산과학기술원에서 만들어졌어. 노인들이 알아들을 수 있게 짧고 친절하게 응답해.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "사과로 할 수 있는 요리 3가지 알려줘."
                }
            ]
        }
    ]
)
print(message.content)