import anthropic

### Posible Models
# claude-3-haiku-20240307
# claude-3-sonnet-20240229
# claude-3-opus-20240229


def text_generate_claude(client, messages):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0,
        system="너는 노인들을 위한 반려로봇이고 너 이름은 '래미'야. 너는 울산과학기술원에서 만들어졌어. 노인들이 알아들을 수 있게 짧고 친절하게 응답해.",
        messages=messages
    )
    
    bot_response = message.content[0].text
    messages.append({"role" : "assistant", "content" : [{"type": "text", "text": f"{bot_response}"}]})
    print(f"LEMMY: {bot_response}")

    return messages


def main():
  client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="YOUR-API-KEY",)
  messages = []

  while True:
    user_input = input('User: ')
    # messages.append({"role" : "user", "content" : f"{user_input}"})
    messages.append({"role" : "user", "content" : [{"type": "text", "text": f"{user_input}"}]})
    messages = text_generate_claude(client, messages)



if __name__ == "__main__":
    main()