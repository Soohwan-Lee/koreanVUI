import time
from openai import OpenAI

client = OpenAI(api_key='YOUR_API_KEY')
dialogueEnd = False
timeout_threshold = 10

def text_generate_GPT(messages):
    global dialogueEnd

    completion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model='gpt-4o',
        messages=messages,
        temperature=0.8
    )

    bot_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": f"{bot_response}"})
    print(f'LEMMY: {bot_response}')

    # Check for keywords indicating end of conversation
    if 'bye' in bot_response.lower() or 'need more help' in bot_response.lower():
        dialogueEnd = True
    
    print(f'(Dialogue End Detection: {dialogueEnd})')
    print("============================")

    return messages

def main():
    global dialogueEnd
    personality = "You are a pet robot for the elderly and your name is LEMMY. You were created at UNIST. You respond in short, friendly sentences that the elderly can understand."
    messages = [{"role": "system", "content": f"{personality}"}]

    while not dialogueEnd:
        try:
            user_input = input_with_timeout('User: ', timeout_threshold)
        except TimeoutError:
            print("\nNo response detected. Ending conversation.")
            dialogueEnd = True
            break

        if user_input.lower() in ['bye', 'no', 'nothing', 'exit']:
            print("Ending conversation as requested by the user.")
            dialogueEnd = True
            break

        messages.append({"role": "user", "content": f"{user_input}"})
        messages = text_generate_GPT(messages)

def input_with_timeout(prompt, timeout):
    import sys, select
    print(prompt, end='', flush=True)
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().strip()
    else:
        raise TimeoutError

if __name__ == "__main__":
    main()
