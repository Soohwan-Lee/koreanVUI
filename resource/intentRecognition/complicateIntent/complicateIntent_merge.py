import requests
import json
import time
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_API_KEY")

def get_weather_info(city, apikey, lang="en", units="metric"):
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units={units}"
    result = requests.get(api)
    if result.status_code != 200:
        return None  # Return None if the API call fails
    data = json.loads(result.text)
    weather_info = {
        "location": data["name"],
        "weather": data["weather"][0]["description"],
        "temperature": {
            "current": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "min": data["main"]["temp_min"],
            "max": data["main"]["temp_max"]
        }
    }
    return weather_info

def get_current_weather(location, unit="celsius"):
    """Get the current weather for the specified location"""
    apikey = "1665f8090ad1a59a2f0e7205979435e6"
    lang = "en"
    weather_info = get_weather_info(location, apikey, lang)
    
    if weather_info is None:
        return json.dumps({"error": f"Unable to fetch weather data for {location}"})
    
    return json.dumps({
        "location": weather_info["location"],
        "temperature": str(weather_info["temperature"]["current"]),
        "weather": weather_info["weather"],
        "unit": unit
    })

def turn_on_air_conditioner():
    """Turn on the air conditioner"""
    print("Air conditioner: ON!!")
    return json.dumps({"status": "Air conditioner turned on"})

def end_conversation():
    """Function to signify the end of the conversation with a nice message."""
    return json.dumps({"message": "Thank you for chatting with me! Have a wonderful day!"})

def generate_response(messages):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "turn_on_air_conditioner",
                "description": "Turn on the air conditioner",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "end_conversation",
                "description": "End the current conversation session with a friendly message such as goodbye, see you, take care, etc.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                },
            },
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.8
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        function_messages = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            if function_name == "get_current_weather":
                function_response = get_current_weather(
                    location=function_args.get("location"),
                    unit=function_args.get("unit", "celsius")
                )
            elif function_name == "turn_on_air_conditioner":
                function_response = turn_on_air_conditioner()
            elif function_name == "end_conversation":
                function_response = end_conversation()
            else:
                raise ValueError(f"Unknown function: {function_name}")

            function_messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })

        messages.append(response_message)
        messages.extend(function_messages)

        # If end_conversation was called, return a special signal
        if any(msg["name"] == "end_conversation" for msg in function_messages):
            return "END_CONVERSATION", messages

        # Call the API again with the function response
        return generate_response(messages)
    else:
        return response_message.content, messages

def main():
    personality = "You are a companion robot for the elderly and your name is LEMMY. You were created at UNIST. You respond in short, friendly sentences that the elderly can understand. You can provide weather information for any city in the world. When you sense that the conversation is coming to a natural end, use the end_conversation function to conclude the chat politely."
    messages = [{"role": "system", "content": personality}]

    # print("LEMMY: Hello! I'm LEMMY. Feel free to ask me about the weather in any city or about the air conditioner.")

    while True:
        user_input = input('USER: ')
        messages.append({"role": "user", "content": user_input})
        bot_response, messages = generate_response(messages)
        
        if bot_response == "END_CONVERSATION":
            final_message = messages[-1]["content"]
            print(f'LEMMY: {json.loads(final_message)["message"]}')
            break
        else:
            print(f'LEMMY: {bot_response}')
            messages.append({"role": "assistant", "content": bot_response})

if __name__ == "__main__":
    main()

# import requests
# import json
# import time
# from openai import OpenAI

# # Initialize OpenAI client
# client = OpenAI(api_key="YOUR_API_KEY")

# def get_weather_info(city, apikey, lang="en", units="metric"):
#     api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units={units}"
#     result = requests.get(api)
#     if result.status_code != 200:
#         return None  # Return None if the API call fails
#     data = json.loads(result.text)
#     weather_info = {
#         "location": data["name"],
#         "weather": data["weather"][0]["description"],
#         "temperature": {
#             "current": data["main"]["temp"],
#             "feels_like": data["main"]["feels_like"],
#             "min": data["main"]["temp_min"],
#             "max": data["main"]["temp_max"]
#         }
#     }
#     return weather_info

# def get_current_weather(location, unit="celsius"):
#     """Get the current weather for the specified location"""
#     apikey = "1665f8090ad1a59a2f0e7205979435e6"
#     lang = "en"
#     weather_info = get_weather_info(location, apikey, lang)
    
#     if weather_info is None:
#         return json.dumps({"error": f"Unable to fetch weather data for {location}"})
    
#     return json.dumps({
#         "location": weather_info["location"],
#         "temperature": str(weather_info["temperature"]["current"]),
#         "weather": weather_info["weather"],
#         "unit": unit
#     })

# def turn_on_air_conditioner():
#     """Turn on the air conditioner"""
#     print("Air conditioner: ON!!")
#     return json.dumps({"status": "Air conditioner turned on"})

# def generate_response(messages):
#     tools = [
#         {
#             "type": "function",
#             "function": {
#                 "name": "get_current_weather",
#                 "description": "Get the current weather in a given location",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "location": {
#                             "type": "string",
#                             "description": "The city name",
#                         },
#                         "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
#                     },
#                     "required": ["location"],
#                 },
#             },
#         },
#         {
#             "type": "function",
#             "function": {
#                 "name": "turn_on_air_conditioner",
#                 "description": "Turn on the air conditioner",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {},
#                     "required": [],
#                 },
#             },
#         }
#     ]

#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=messages,
#         tools=tools,
#         tool_choice="auto",
#         temperature=0.8
#     )

#     response_message = response.choices[0].message
#     tool_calls = response_message.tool_calls

#     if tool_calls:
#         function_messages = []
#         for tool_call in tool_calls:
#             function_name = tool_call.function.name
#             function_args = json.loads(tool_call.function.arguments)

#             if function_name == "get_current_weather":
#                 function_response = get_current_weather(
#                     location=function_args.get("location"),
#                     unit=function_args.get("unit", "celsius")
#                 )
#             elif function_name == "turn_on_air_conditioner":
#                 function_response = turn_on_air_conditioner()
#             else:
#                 raise ValueError(f"Unknown function: {function_name}")

#             function_messages.append({
#                 "tool_call_id": tool_call.id,
#                 "role": "tool",
#                 "name": function_name,
#                 "content": function_response,
#             })

#         messages.append(response_message)
#         messages.extend(function_messages)

#         # Call the API again with the function response
#         return generate_response(messages)
#     else:
#         return response_message.content

# def main():
#     personality = "You are a companion robot for the elderly and your name is LEMMY. You were created at Ulsan Institute of Science and Technology. You respond in short, friendly sentences that the elderly can understand. You can provide weather information for any city in the world."
#     messages = [{"role": "system", "content": personality}]

#     # print("LEMMY: Hello! I'm LEMMY. Feel free to ask me about the weather in any city or about the air conditioner.")

#     while True:
#         user_input = input('USER: ')
#         # if user_input.lower() in ['quit', 'exit']:
#         #     print("LEMMY: Goodbye! Take care!")
#         #     break
#         messages.append({"role": "user", "content": user_input})
#         bot_response = generate_response(messages)
#         print(f'LEMMY: {bot_response}')
#         messages.append({"role": "assistant", "content": bot_response})

# if __name__ == "__main__":
#     main()









#### 아래 코드는 울산 지역 날씨 정보를 JSON으로 저장했다가 다시 불러오는 코드
# import requests
# import json
# import time
# from openai import OpenAI

# # Initialize OpenAI client
# client = OpenAI(api_key="YOUR_API_KEY")

# def get_weather_info(city, apikey, lang="en", units="metric"):
#     api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units={units}"
#     result = requests.get(api)
#     data = json.loads(result.text)
#     weather_info = {
#         "location": data["name"],
#         "weather": data["weather"][0]["description"],
#         "temperature": {
#             "current": data["main"]["temp"],
#             "feels_like": data["main"]["feels_like"],
#             "min": data["main"]["temp_min"],
#             "max": data["main"]["temp_max"]
#         }
#     }
#     return weather_info

# def save_weather_info(weather_info, filename="weather_info.json"):
#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(weather_info, f, ensure_ascii=False, indent=4)

# def fetch_and_save_weather():
#     city = "Ulsan"
#     apikey = "1665f8090ad1a59a2f0e7205979435e6"
#     lang = "en"
#     weather_info = get_weather_info(city, apikey, lang)
#     save_weather_info(weather_info)
#     print("Weather information updated and saved.")
#     return weather_info

# def get_current_weather(location, unit="celsius"):
#     """Get the current weather from the saved JSON file"""
#     with open("weather_info.json", "r", encoding="utf-8") as f:
#         weather_info = json.load(f)
#     return json.dumps({
#         "location": weather_info["location"],
#         "temperature": str(weather_info["temperature"]["current"]),
#         "unit": unit
#     })

# def turn_on_air_conditioner():
#     """Turn on the air conditioner"""
#     print("Air conditioner: ON!!")
#     return json.dumps({"status": "Air conditioner turned on"})

# def generate_response(messages):
#     tools = [
#         {
#             "type": "function",
#             "function": {
#                 "name": "get_current_weather",
#                 "description": "Get the current weather in a given location",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "location": {
#                             "type": "string",
#                             "description": "The city, e.g. Ulsan, Seoul and Changwon",
#                         },
#                         "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
#                     },
#                     "required": ["location"],
#                 },
#             },
#         },
#         {
#             "type": "function",
#             "function": {
#                 "name": "turn_on_air_conditioner",
#                 "description": "Turn on the air conditioner",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {},
#                     "required": [],
#                 },
#             },
#         }
#     ]

#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=messages,
#         tools=tools,
#         tool_choice="auto",
#         temperature=0.8
#     )

#     response_message = response.choices[0].message
#     tool_calls = response_message.tool_calls

#     if tool_calls:
#         function_messages = []
#         for tool_call in tool_calls:
#             function_name = tool_call.function.name
#             function_args = json.loads(tool_call.function.arguments)

#             if function_name == "get_current_weather":
#                 function_response = get_current_weather(
#                     location=function_args.get("location"),
#                     unit=function_args.get("unit")
#                 )
#             elif function_name == "turn_on_air_conditioner":
#                 function_response = turn_on_air_conditioner()
#             else:
#                 raise ValueError(f"Unknown function: {function_name}")

#             function_messages.append({
#                 "tool_call_id": tool_call.id,
#                 "role": "tool",
#                 "name": function_name,
#                 "content": function_response,
#             })

#         messages.append(response_message)
#         messages.extend(function_messages)

#         # Call the API again with the function response
#         return generate_response(messages)
#     else:
#         return response_message.content

# def main():
#     # Fetch and save weather information at the start
#     fetch_and_save_weather()

#     personality = "You are a companion robot for the elderly and your name is LEMMY. You were created at UNIST. You respond in short, friendly sentences that the elderly can understand. You have access to current weather information for Ulsan."
#     messages = [{"role": "system", "content": personality}]

#     # print("LEMMY: Hello! I'm LEMMY. I've just updated the weather information. Feel free to ask me about the weather in Ulsan or about the air conditioner.")

#     while True:
#         user_input = input('USER: ')
#         if user_input.lower() in ['quit', 'exit']:
#             print("LEMMY: Goodbye! Take care!")
#             break
#         messages.append({"role": "user", "content": user_input})
#         bot_response = generate_response(messages)
#         print(f'LEMMY: {bot_response}')
#         messages.append({"role": "assistant", "content": bot_response})

# if __name__ == "__main__":
#     main()

