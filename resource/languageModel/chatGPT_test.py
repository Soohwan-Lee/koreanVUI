import openai
import json
import os

#API 키 입력
# openai.api_key = os.environ["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"]
#API 키 입력
openai.api_key = "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"

user_query = '사과는 무슨 색인가요?'
response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages=[{"role": "user", "content": user_query}])
print(response.choices[0].message['content'])
response2 = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages=[{"role": "system","content":"너는 노인들을 위한 반려로봇이야. 굉장히 공손하고 친절한 말투로 응답을 해야해."},
                                                                            {"role": "user", "content": user_query}])
print(response2.choices[0].message['content'])

# # 호출 함수
# def get_price_info(product_name):    
#     # 가격 정보₩₩
#     product_price = {"키보드": "3만원", "마우스": "2만원", "모니터": "30만원"}
    
#     prince = product_price.get(product_name) # 제품 이름을 입력해 가격 가져오기
#     if prince == None: # 제품 가격이 없을 경우
#         prince = "해당 상품은 가격 정보가 없습니다."

#     price_info = {
#         "product_name": product_name,
#         "price": prince
#     }
    
#     return json.dumps(price_info)

# # Chat Completions API를 이용해 사용자 입력에 따라 함수를 호출하고 응답하는 함수
# def run_conversation(user_query):
#     # 사용자 입력
#     messages = [{"role": "user", "content": user_query}] 
        
#     # 함수 정보 입력   
#     functions = [                                        
#         {
#             "name": "get_price_info",
#             "description": "제품 이름에 따른 가격 가져오기",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "product_name": {
#                         "type": "string",
#                         "description": "제품 이름. 예를 들면, 키보드, 마우스",
#                     },
#                 },
#                 "required": ["product_name"],
#             },
#         }
#     ]
#     # 1단계: 사용자 입력과 함수 정보를 Chat Completions API 모델로 보내기    
#     response = openai.ChatCompletion.create( # Chat Completions API 모델로 보내기
#             model="gpt-3.5-turbo",
#             # model="gpt-4",
#             messages=messages,
#             functions=functions,
#             function_call="auto"
#     )
#     # 2단계: 응답 생성
#     response_message = response["choices"][0]["message"] # 모델의 응답 메시지
    
#     if response_message.get("function_call"): # 응답이 함수 호출인지 확인하기
#         # 3단계: JSON 객체를 분석해 함수 이름과 인수를 추출한 후에 함수 호출
#         # (주의: JSON 응답이 항상 유효하지 않을 수 있음)
        
#         # 함수 이름 추출
#         function_name = response_message["function_call"]["name"]
#         # 함수 호출을 위한 인수 추출
#         function_args = json.loads(response_message["function_call"]["arguments"])
        
#         # 함수 호출 및 반환 결과 받기
#         function_response = get_price_info(
#             product_name=function_args.get("product_name") # 인수 지정
#         )
        
#         # 4단계: 함수 호출 결과를 기존 메시지에 추가하고,
#         #        Chat Completions API 모델로 보내 응답받기

#         # 함수 호출 결과를 기존 메시지에 추가하기
#         messages.append(response_message)  # 기존 messages에 조력자 응답 추가
#         messages.append(                   # 함수와 함수 호출 결과 추가
#             {
#                 "role": "function",           # role: function으로 지정
#                 "name": function_name,        # name: 호출할 함수 이름 지정
#                 "content": function_response, # content: 함수 호출 결과 지정
#             }
#         )
#         # 함수 호출 결과를 추가한 메시지를 Chat Completions API 모델로 보내 응답받기
#         second_response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             # model="gpt-4",
#             messages=messages,
#         ) 
#         return second_response # 두 번째 응답 반환
    
#     return response_message # 응답 메시지 반환

# user_query = '마우스 가격은 얼마인가요?'
# response = run_conversation(user_query)
# # print(response)
# print(response.choices[0].message['content'])