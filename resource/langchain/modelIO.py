from langchain.memory import ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# YOUR_API_KEY
llm = ChatOpenAI(model="gpt-4o", temperature=0.1, api_key="YOUR_API_KEY")

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=80,
    memory_key="chat_history",
    return_messages=True,
)

def load_memory(input):
    print(input)
    return memory.load_memory_variables({})["chat_history"]
    
prompt = ChatPromptTemplate.from_messages([
    ("system", "Your name is LEMMY and you're a social robot for seniors. You were created at UNIST. You answer questions in a friendly, concise way that seniors can understand."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

chain = RunnablePassthrough.assign(chat_history=load_memory) | prompt | llm

def invoke_chain(question):
    result = chain.invoke({"question": question})
    memory.save_context(
        {"input": question},
        {"output": result.content},
    )
    print(result.content)
    print("===================")

def main():
    # invoke_chain("My name is nam.")
    # invoke_chain("What's my name?")

    while True:
        user_input = input('User: ')
        invoke_chain(user_input)


if __name__ == "__main__":
    main()