from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Create OpenAI Chat "YOUR_API_KEY"
chat = ChatOpenAI(model="gpt-4o", api_key="YOUR_API_KEY")

# Create New Chat Message History
chat_history = ChatMessageHistory()

chat_history.add_user_message("안녕하세요. 제 이름은 제이크입니다.")
chat_history.add_ai_message("안녕하세요, 제이크 님! 무엇을 도와드릴까요?")
chat_history.add_user_message("날씨 좋은 날 들을만 한 노래 추천해주세요.")
chat_history.add_ai_message("Carpenters - Close to you 를 추천해요.")

print(chat_history)

# ChatMessageHistory 객체를 Runnable하게 선언 -> RunnableWithMessageHistory
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful social robot, Lemmy. Answer all questions to the best of your ability. The provided chat history includes facts about the user you are speaking with. YOU MUST ANSWER IN KOREAN.",
        ),
        ("placeholder", "{chat_history}"),
        ("user", "{input}"),
    ]
)

chain = prompt | chat

chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: chat_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# 전역 변수로 현재 요약 내용을 저장
current_summary = ""

# Summarization 함수 선언
def summarize_messages(chain_input):
    global current_summary
    stored_messages = chat_history.messages
    if len(stored_messages) == 0:
        return False
    summarization_prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            (
                "user",
                "Distill the above chat messages into a single summary message. Include as many specific details as you can.",
            ),
        ]
    )
    summarization_chain = summarization_prompt | chat

    # chat_history 에 저장된 대화 기록을 요약프롬프트에 입력 & 결과 저장
    summary_message = summarization_chain.invoke({"chat_history": stored_messages})
    
    # 현재 요약 내용 업데이트
    current_summary = summary_message.content

    # chat_history 에 저장되어있던 기록 지우기
    chat_history.clear()

    # 생성된 새로운 요약내용으로 기록 채우기
    chat_history.add_message(summary_message)

    return True

chain_with_summarization = (
    RunnablePassthrough.assign(messages_summarized=summarize_messages)
    | chain_with_message_history
)

if __name__ == "__main__":
    while True:
        print("============== New Conversation Turn ==============")
        user_input = input("🗣️ USER's INPUT: ")
        ai_output = chain_with_summarization.invoke(
            {"input": user_input},
            {"configurable": {"session_id": "unused"}},
        )
        print("🤖 AI's RESPONSE: " + ai_output.content)
        print(f"(💭 Current Summarized Memory: {current_summary})")
