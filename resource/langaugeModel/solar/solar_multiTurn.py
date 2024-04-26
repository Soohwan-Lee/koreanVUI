from openai import OpenAI # openai==1.2.0
 
client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v1/solar"
)

def text_generate_solar(messages):
    stream = client.chat.completions.create(
        model="solar-1-mini-chat",
        messages=messages,
        stream=False,
    )

    bot_response = stream.choices[0].message.content
    messages.append({"role" : "assistant", "content" : f"{bot_response}"})
    print(f'LEMMY: {bot_response}')

    return messages



def main():
  personality = "너는 노인들을 위한 반려로봇이고 너 이름은 '래미'야. 너는 울산과학기술원에서 만들어졌어. 노인들이 알아들을 수 있게 짧고 친절하게 응답해."
  messages = [{"role" : "system", "content" : f"{personality}"}]

  while True:
    user_input = input('User: ')
    messages.append({"role" : "user", "content" : f"{user_input}"})
    messages = text_generate_solar(messages)



if __name__ == "__main__":
    main()


### Use with stream=True
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")
 
### Use with stream=False
# print(stream.choices[0].message.content)