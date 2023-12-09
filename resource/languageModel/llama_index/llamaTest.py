import os
import platform

from openai import OpenAI
import chromadb
import langchain
import tiktoken
import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ChatVectorDBChain
from langchain.document_loaders import GutenbergLoader

# client = OpenAI(api_key="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")
os.environ["OPENAI_API_KEY"] = "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"

# llama_index 모듈에서 SimpleDirectoryReader와 download_loader를 import합니다.
from llama_index import SimpleDirectoryReader, download_loader  

# download_loader 함수를 이용하여 SimpleDirectoryReader를 다운로드합니다.
SimpleDirectoryReader = download_loader("SimpleDirectoryReader")

# './data' 디렉토리에서 재귀적으로 모든 파일을 읽어들이고 숨겨진 파일은 제외합니다.  
loader = SimpleDirectoryReader('./resource/languageModel/llama_index/data', recursive=True, exclude_hidden=True)  

# documents 변수에 loader.load_data()를 통해 데이터를 로드합니다.
documents = loader.load_data()

# llama_index 모듈에서 LLMPredictor, GPTSimpleVectorIndex, PromptHelper, ServiceContext와 langchain 모듈에서 OpenAI를 import합니다.
from llama_index import LLMPredictor, GPTVectorStoreIndex, PromptHelper, ServiceContext
from langchain import OpenAI

# OpenAI의 text-davinci-003 모델을 사용하여 LLMPredictor를 정의합니다.
llm_predictor = LLMPredictor(llm=langchain.llms.OpenAI(temperature=0, model_name="text-davinci-003"))

# PromptHelper를 정의합니다.
max_input_size = 3900
num_output = 256
max_chunk_overlap = 0.2
prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

# ServiceContext를 정의합니다.
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

# 앞서 PDF를 로드한 documents를 사용하여 GPTSimpleVectorIndex를 정의합니다.
index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

from llama_index import StorageContext, load_index_from_disk
# 로컬 디스크에 인덱스 저장하기
# index.save_to_disk('index.json')
index.storage_context.persist(persist_dir="./resource/languageModel/llama_index/index.json")

# 로컬 디스크에서 인덱스 불러오기
# index = GPTVectorStoreIndex.load_from_disk('index.json')
loaded_index = load_index_from_disk(StorageContext.from_defaults(persist_dir="./resource/languageModel/llama_index/index.json"))


response = index.query("유토피아가 뭔지 알려주세요.")
print(response.response)