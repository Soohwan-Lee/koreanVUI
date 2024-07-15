import time
from openai import OpenAI
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re

nltk.download('vader_lexicon')

# YOUR_API_KEY
client = OpenAI(api_key='YOUR_API_KEY')
dialogueEnd = False
sentiment_analyzer = SentimentIntensityAnalyzer()
timeout_threshold = 10

def text_generate_GPT(messages):
    global dialogueEnd

    completion = client.chat.completions.create(
        model='gpt-4o',
        messages=messages,
        temperature=0.8
    )

    bot_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": f"{bot_response}"})
    print(f'LEMMY: {bot_response}')

    # Check for keywords indicating end of conversation
    if any(phrase in bot_response.lower() for phrase in end_conversation_phrases):
        dialogueEnd = True
        print("Conversation ended due to assistant detecting an end phrase.")

    return messages

def analyze_sentiment(user_input):
    sentiment_score = sentiment_analyzer.polarity_scores(user_input)['compound']
    return sentiment_score

def main():
    global dialogueEnd
    personality = "You are a pet robot for the elderly and your name is LEMMY. You were created at UNIST. You respond in short, friendly sentences that the elderly can understand."
    messages = [{"role": "system", "content": f"{personality}"}]

    consecutive_neutral_negative = 0

    while not dialogueEnd:
        try:
            user_input = input_with_timeout('User: ', timeout_threshold)
        except TimeoutError:
            print("\nNo response detected. Ending conversation due to timeout.")
            dialogueEnd = True
            break

        if any(phrase in user_input.lower() for phrase in end_conversation_phrases):
            dialogueEnd = True
            print("Ending conversation as requested by the user.")
            break

        sentiment_score = analyze_sentiment(user_input)
        if sentiment_score <= 0:
            consecutive_neutral_negative += 1
        else:
            consecutive_neutral_negative = 0

        if consecutive_neutral_negative >= 3:
            print("Ending conversation based on consecutive neutral/negative responses.")
            dialogueEnd = True
            break

        messages.append({"role": "user", "content": f"{user_input}"})
        messages = text_generate_GPT(messages)

end_conversation_phrases = [
    'bye', 'goodbye', 'see you', 'exit', 'quit', 'take care'#, 'no', 'nothing', 
    #'thanks', 'thank you', 'that\'s all', 'I\'m done', 'stop', 'enough', 'terminate'
]

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