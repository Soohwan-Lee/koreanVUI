# from gpt_index import SimpleDirectoryReader, GPTListIndex,readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
from types import FunctionType
from llama_index import ServiceContext, GPTVectorStoreIndex, LLMPredictor, PromptHelper, SimpleDirectoryReader, load_index_from_storage
import sys
import os
import time 
import langchain


os.environ["OPENAI_API_KEY"] = "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"
from llama_index.node_parser import SimpleNodeParser

from llama_index import StorageContext, load_index_from_storage
from langchain.chat_models import ChatOpenAI
parser = SimpleNodeParser()




def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 500
    max_chunk_overlap = 0.2
    chunk_size_limit = 1024

    print("*"*5, "Documents parsing initiated", "*"*5)
    file_metadata = lambda x : {"filename": x}
    reader = SimpleDirectoryReader(directory_path, file_metadata=file_metadata)
    documents = reader.load_data()
    
  
    # nodes = parser.get_nodes_from_documents(documents)
    # index = GPTVectorStoreIndex(nodes)
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=langchain.llms.OpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
    
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    # print("*"*5, "Index creation initiated", "*"*5)
    index = GPTVectorStoreIndex.from_documents(
        documents=documents, service_context = service_context
    )
    # print("*"*5, "Index created", "*"*5)
    index.storage_context.persist("./resource/languageModel/llama_index/data")
    return index
    
construct_index("./resource/languageModel/llama_index/data")
storage_context = StorageContext.from_defaults(persist_dir="./resource/languageModel/llama_index/data")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()
while True:
    # text_input = input("YOU : ")
    text_input = "유토피아가 뭔가요? 짧게 설명해주세요."
    response = query_engine.query(text_input)
    print("Bot : ", response)
    print('\n')