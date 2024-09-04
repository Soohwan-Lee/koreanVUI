import os
from tavily import TavilyClient
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

# Set your API keys here YOUR_API_KEY
OPENAI_API_KEY = "YOUR_API_KEY"
TAVILY_API_KEY = "YOUR_API_KEY"

# Initialize the Tavily Client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Configure the ChatOpenAI model in LangChain
chat_llm = ChatOpenAI(model="gpt-4", temperature=0.7, openai_api_key=OPENAI_API_KEY)

# Define a prompt template for the interaction
prompt_template = PromptTemplate(
    input_variables=["input"],
    template="{input}"
)

# Create a LangChain LLMChain using the ChatOpenAI model
llm_chain = LLMChain(llm=chat_llm, prompt=prompt_template)

# Tavily API interaction function using Tavily SDK
def get_tavily_data(query):
    try:
        # Perform a search using the Tavily SDK
        response = tavily_client.search(query)
        # Extract and return the most relevant answer
        if response['results']:
            top_result = response['results'][0]
            return f"{top_result['title']}: {top_result['content']}"
        else:
            return "No relevant information found."
    except Exception as err:
        return f"An error occurred: {err}"

# Function to summarize Tavily's result with GPT-4
def summarize_with_gpt(question, result_text):
    gpt_prompt = f"Based on the following information, provide a concise answer to the question '{question}':\n\n{result_text}\n\nAnswer in one sentence."
    gpt_response = llm_chain.invoke({"input": gpt_prompt})
    return gpt_response['text']

def main():
    print("Welcome to the LangChain GPT-4 and Tavily interaction terminal!")
    print("Type your query and hit Enter. Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break

        # Check if the user wants to use Tavily API
        if "tavily" in user_input.lower():
            query = user_input.replace("tavily", "").strip()
            tavily_response = get_tavily_data(query)
            summarized_response = summarize_with_gpt(user_input, tavily_response)
            print(f"Tavily (via GPT-4): {summarized_response}")
        else:
            # Pass user input to GPT-4 using LangChain's ChatOpenAI
            gpt_response = llm_chain.invoke({"input": user_input})
            print(f"GPT-4: {gpt_response['text']}")
        print("="*30)
if __name__ == "__main__":
    main()
