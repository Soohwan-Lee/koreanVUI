from openai import OpenAI
client = OpenAI(api_key='YOUR_API_KEY')

def text_generate_GPT(messages):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.8
  )

  print(completion)
  test = completion.choices[0].message
  print(test.content)
  bot_response = completion.choices[0].message.content
  messages.append({"role" : "assistant", "content" : f"{bot_response}"})
  print(f'LEMMY: {bot_response}')

  return messages


def main():
  personality = "너는 노인들을 위한 반려로봇이고 너 이름은 '래미'야. 너는 울산과학기술원에서 만들어졌어. 노인들이 알아들을 수 있게 짧고 친절하게 응답해."
  # personality = "You are a social robot for the elderly and your name is Rami. You were created at UNIST. You respond in short, friendly sentences that the elderly can understand."
  messages = [{"role" : "system", "content" : f"{personality}"}]

  while True:
    user_input = input('User: ')
    messages.append({"role" : "user", "content" : f"{user_input}"})
    messages = text_generate_GPT(messages)



if __name__ == "__main__":
    main()