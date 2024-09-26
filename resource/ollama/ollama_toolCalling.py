import ollama
import json

def get_korea_weather(location):
    """Get the current weather for Seoul, Ulsan, or Changwon"""
    print('Debug - get_korea_weather function called with location:', location)
    weather_data = {
        "seoul": {"temperature": 25, "condition": "Sunny"},
        "ulsan": {"temperature": 28, "condition": "Partly cloudy"},
        "changwon": {"temperature": 27, "condition": "Cloudy"}
    }
    location = location.lower()
    if location in weather_data:
        return json.dumps({
            "location": location.capitalize(),
            "temperature": weather_data[location]['temperature'],
            "condition": weather_data[location]['condition']
        })
    else:
        return json.dumps({"error": f"No weather information available for {location.capitalize()}."})

def run_conversation(messages):
    response = ollama.chat(
        model='llama3.1', 
        messages=messages,
        stream=False,
        tools=[{
            "type": "function",
            "function": {
                "name": "get_korea_weather",
                "description": "Get the current weather for Seoul, Ulsan, or Changwon",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "enum": ["Seoul", "Ulsan", "Changwon"]
                        }
                    },
                    "required": ["location"]
                }
            }
        }]
    )

    # print("Debug - Response:", response)  # 디버그 출력 추가

    if 'message' in response and 'tool_calls' in response['message'] and any(tc['function']['name'].lower() != 'none' for tc in response['message']['tool_calls']):
        # print("CHECK 1")
        for tool_call in response['message']['tool_calls']:
            if tool_call['function']['name'].lower() == 'get_korea_weather':
                args = tool_call['function']['arguments']
                if isinstance(args, str):
                    args = json.loads(args)
                elif not isinstance(args, dict):
                    raise ValueError(f"Unexpected arguments type: {type(args)}")

                if 'location' in args:
                    weather_info = get_korea_weather(args['location'])
                    messages.append({
                        "role": "function",
                        "name": "get_korea_weather",
                        "content": weather_info
                    })
                    # 날씨 정보를 포함하여 응답하도록 요청
                    messages.append({
                        "role": "user",
                        "content": f"Please respond with this weather information: {weather_info}"
                    })
                else:
                    print(f"Error: Invalid arguments structure: {args}")
        
        # 날씨 정보를 포함한 최종 응답 얻기
        final_response = ollama.chat(
            model='llama3.1',
            messages=messages,
            stream=False
        )
        # print("Debug - Final Response:", final_response)  # 디버그 출력 추가
        return final_response['message']['content']
    elif 'message' in response and 'content' in response['message']:
        # print("CHECK 2")
        return response['message']['content']
    else:
        return "I'm sorry, I'm having trouble formulating a response. Could you please rephrase your question?"

def main():
    system_message = "You are a social robot for the elderly named Lemmy. You were created at UNIST. Respond in short, friendly sentences that the elderly can understand. Only use the get_korea_weather function when explicitly asked about the weather in Seoul, Ulsan, or Changwon."
    
    messages = [{"role": "system", "content": system_message}]
    
    print("Chat with Lemmy (type 'exit' to end the conversation)")
    while True:
        user_input = input('User: ')
        if user_input.lower() == 'exit':
            break
        
        messages.append({"role": "user", "content": user_input})
        response = run_conversation(messages)
        messages.append({"role": "assistant", "content": response})
        
        print(f'Lemmy: {response}')
        print("="*100)


if __name__ == "__main__":
    main()

# import ollama
# import json
# import re
# import ast  # Add this import

# def get_korea_weather(location):
#     """Get the current weather for Seoul, Ulsan, or Changwon"""
#     weather_data = {
#         "seoul": {"temperature": 25, "condition": "Sunny"},
#         "ulsan": {"temperature": 28, "condition": "Partly cloudy"},
#         "changwon": {"temperature": 27, "condition": "Cloudy"}
#     }
#     location = location.lower()
#     if location in weather_data:
#         return json.dumps({
#             "location": location.capitalize(),
#             "temperature": weather_data[location]['temperature'],
#             "condition": weather_data[location]['condition']
#         })
#     else:
#         return json.dumps({"error": f"No weather information available for {location.capitalize()}."})

# def run_conversation(user_input):
#     system_message = "You are a social robot for the elderly named Lemmy. You were created at UNIST. Respond in short, friendly sentences that the elderly can understand. If asked about weather in Seoul, Ulsan, or Changwon, use the get_korea_weather function and include the information in your response."
    
#     messages = [
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": user_input}
#     ]

#     response = ollama.chat(
#         model='llama3.1', 
#         messages=messages,
#         stream=False,
#         tools=[{
#             "type": "function",
#             "function": {
#                 "name": "get_korea_weather",
#                 "description": "Get the current weather for Seoul, Ulsan, or Changwon",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "location": {
#                             "type": "string",
#                             "enum": ["Seoul", "Ulsan", "Changwon"]
#                         }
#                     },
#                     "required": ["location"]
#                 }
#             }
#         }]
#     )

#     if 'message' in response and 'tool_calls' in response['message']:
#         for tool_call in response['message']['tool_calls']:
#             if tool_call['function']['name'] == 'get_korea_weather':
#                 args = tool_call['function']['arguments']
#                 if isinstance(args, str):
#                     try:
#                         args = json.loads(args)
#                     except json.JSONDecodeError:
#                         try:
#                             args = ast.literal_eval(args)
#                         except (ValueError, SyntaxError):
#                             location_match = re.search(r'"location"\s*:\s*"(\w+)"', args)
#                             args = {"location": location_match.group(1)} if location_match else {}
                
#                 if isinstance(args, dict) and 'location' in args:
#                     weather_info = get_korea_weather(args['location'])
#                     messages.append({
#                         "role": "function",
#                         "name": "get_korea_weather",
#                         "content": weather_info
#                     })
#                     # 날씨 정보를 포함하여 응답하도록 요청
#                     messages.append({
#                         "role": "user",
#                         "content": f"Please respond to my previous question and include this weather information: {weather_info}"
#                     })
#                 else:
#                     print(f"Error: Invalid arguments structure: {args}")

#         # 날씨 정보를 포함한 최종 응답 얻기
#         final_response = ollama.chat(
#             model='llama3.1',
#             messages=messages,
#             stream=False
#         )
#         return final_response['message']['content']
#     elif 'message' in response and 'content' in response['message']:
#         return response['message']['content']
#     else:
#         return "I'm sorry, I'm having trouble formulating a response. Could you please rephrase your question?"

# def main():
#     print("Chat with Lemmy (type 'exit' to end the conversation)")
#     while True:
#         print("="*100)
#         user_input = input('User: ')
#         if user_input.lower() == 'exit':
#             break
        
#         response = run_conversation(user_input)
#         print(f'Lemmy: {response}')

# if __name__ == "__main__":
#     main()


########################################################
# import ollama
# import json

# def get_korea_weather(city):
#     """Get the current weather for Seoul, Ulsan, or Changwon"""
#     weather_data = {
#         "seoul": {"temperature": 25, "condition": "Sunny"},
#         "ulsan": {"temperature": 28, "condition": "Partly cloudy"},
#         "changwon": {"temperature": 27, "condition": "Cloudy"}
#     }
#     city = city.lower()
#     if city in weather_data:
#         return f"The weather in {city.capitalize()} is {weather_data[city]['condition']} with a temperature of {weather_data[city]['temperature']}°C."
#     else:
#         return f"Sorry, I don't have weather information for {city.capitalize()}."

# def main():
#     system_message = {
#         "role": "system",
#         "content": "You are a social robot for the elderly named Lemmy. You were created at UNIST. Respond in short, friendly sentences that the elderly can understand. If asked about weather in Seoul, Ulsan, or Changwon, use the get_korea_weather function and include the information in your response."
#     }
    
#     messages = [system_message]
    
#     print("Chat with Lemmy (type 'exit' to end the conversation)")
#     while True:
#         user_input = input('User: ')
#         if user_input.lower() == 'exit':
#             break
        
#         messages.append({"role": "user", "content": user_input})
        
#         response = ollama.chat(model='llama3.1', messages=messages, stream=False, tools=[{
#             "type": "function",
#             "function": {
#                 "name": "get_korea_weather",
#                 "description": "Get the current weather for Seoul, Ulsan, or Changwon",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "city": {
#                             "type": "string",
#                             "enum": ["Seoul", "Ulsan", "Changwon"]
#                         }
#                     },
#                     "required": ["city"]
#                 }
#             }
#         }])
        
#         if 'message' in response:
#             if 'tool_calls' in response['message']:
#                 for tool_call in response['message']['tool_calls']:
#                     if tool_call['function']['name'] == 'get_korea_weather':
#                         args = tool_call['function']['arguments']
#                         if isinstance(args, dict) and 'city' in args:
#                             weather_info = get_korea_weather(args['city'])
#                             messages.append({
#                                 "role": "function",
#                                 "name": "get_korea_weather",
#                                 "content": weather_info
#                             })
#                             # Add a user message to prompt for a response including the weather info
#                             messages.append({
#                                 "role": "user",
#                                 "content": f"Please respond to my previous question and include this weather information: {weather_info}"
#                             })
#                             # Get a new response after adding the function result
#                             response = ollama.chat(model='llama3.1', messages=messages, stream=False)
            
#             if 'content' in response['message']:
#                 assistant_message = response['message']['content']
#                 if assistant_message.strip():
#                     print(f'Lemmy: {assistant_message}')
#                     messages.append({"role": "assistant", "content": assistant_message})
#                 else:
#                     print("Lemmy: I'm sorry, I don't have a specific response for that. Is there anything else I can help you with?")
#             else:
#                 print("Lemmy: I apologize, I'm having trouble formulating a response. Could you please rephrase your question?")
#         else:
#             print("Error: Unexpected response format")
#             print("Debug - Response structure:", json.dumps(response, indent=2))

# if __name__ == "__main__":
#     main()

