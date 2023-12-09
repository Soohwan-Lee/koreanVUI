from langchain.retrievers.web_research import WebResearchRetriever
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models.openai import ChatOpenAI
from langchain.utilities import GoogleSearchAPIWrapper

os.environ["GOOGLE_CSE_ID"] = "XXX"
os.environ["GOOGLE_API_KEY"] = "XXX"
os.environ["OPENAI_API_KEY"] = "XXX"

# Vectorstore 셋팅하기
vectorstore = Chroma(embedding_function=OpenAIEmbeddings(),
                     persist_directory="./chroma_db_oai")

# Search Query를 위한 LLM
search_llm = ChatOpenAI(temperature=0)

# SearchAPI Wrapper 객체 생성하기
search = GoogleSearchAPIWrapper()

# Web Research Retriever 셋팅하기
web_research_retriever = WebResearchRetriever.from_llm(
    vectorstore=vectorstore,
    llm=search_llm, 
    search=search, 
)

from langchain.chains import RetrievalQAWithSourcesChain
response_llm = ChatOpenAI(temperature=0.90)
qa_chain = RetrievalQAWithSourcesChain.from_chain_type(response_llm,
                                                       retriever=web_research_retriever)

user_input = "오늘 날씨 뭐야?"
result = qa_chain({"question": user_input})
result