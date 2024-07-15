from openai import OpenAI
import json

# YOUR_API_KEYS
client = OpenAI(api_key="YOUR_API_KEY")

# Example dummy function hard coded to return the same weather
def get_current_weather(location, unit="celsius"):
    """Get the current weather in a given location"""
    print("Get Current Weather!!")
    if "ulsan" in location.lower():
        return json.dumps({"location": "Ulsan", "temperature": "30", "unit": unit})
    elif "seoul" in location.lower():
        return json.dumps({"location": "Seoul", "temperature": "29", "unit": unit})
    elif "changwon" in location.lower():
        return json.dumps({"location": "Changwon", "temperature": "25", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

def turn_on_air_conditioner():
    """Turn on the air conditioner"""
    print("Air conditioner: ON!!")
    return json.dumps({"status": "Air conditioner turned on"})

def run_conversation():
    # Initial message from user
    messages = [{"role": "user", "content": "If the weather in Ulsan is above 28 degrees, please turn on the air conditioner."}]

    # Available tools for the model to use
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
                            "description": "The city, e.g. Ulsan, Seoul and Changwon",
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
        }
    ]

    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.8
        )

        print("CheckPoint 1: ")
        print(response)

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.append(response_message)  # Add assistant's message to the conversation

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name == "get_current_weather":
                    function_response = get_current_weather(
                        location=function_args.get("location"),
                        unit=function_args.get("unit")
                    )
                elif function_name == "turn_on_air_conditioner":
                    function_response = turn_on_air_conditioner()
                else:
                    raise ValueError(f"Unknown function: {function_name}")

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
                print(f"CheckPoint 2: ")
                print(messages)


        else:
            # If there are no more function calls, we're done
            print(f"CheckPoint 3: ")
            print(messages)
            messages.append(response_message)
            break

    return response_message.content

print(run_conversation())







# from openai import OpenAI
# import json

# # YOUR_API_KEY
# client = OpenAI(api_key="YOUR_API_KEY")

# # Example dummy function hard coded to return the same weather
# # In production, this could be your backend API or an external API
# def get_current_weather(location, unit="fahrenheit"):
#     """Get the current weather in a given location"""
#     if "ulsan" in location.lower():
#         return json.dumps({"location": "Ulsan", "temperature": "25", "unit": unit})
#     elif "seoul" in location.lower():
#         return json.dumps({"location": "Seoul", "temperature": "27", "unit": unit})
#     elif "chagwon" in location.lower():
#         return json.dumps({"location": "Changwon", "temperature": "22", "unit": unit})
#     else:
#         return json.dumps({"location": location, "temperature": "unknown"})

# def turn_on_air_conditioner():
#     """Turn on the air conditioner"""
#     return json.dumps({"status": "Air conditioner turned on"})

# def run_conversation():
#     # Step 1: send the conversation and available functions to the model
#     messages = [{"role": "user", "content": "What's the weather like today??"}]
#     tools = [
#         {
#             "type": "function",
#             "function": {
#                 "name": "get_current_weather",
#                 "description": "Get weather information for specific location, such as Ulsan, Seoul, and Changwon.",
#                 "parameters": {
#                     "type": "object", 
#                     "properties": {
#                         "location": {
#                             "type": "string",
#                             "description": "City name, for example Ulsan, Seoul, Changwon",
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
#         },
#     ]
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=messages,
#         tools=tools,
#         tool_choice="auto",  # auto is default, but we'll be explicit
#     )
#     response_message = response.choices[0].message
#     tool_calls = response_message.tool_calls
#     print(response_message)
#     # Step 2: check if the model wanted to call a function
#     if tool_calls:
#         # Step 3: call the function
#         # Note: the JSON response may not always be valid; be sure to handle errors
#         available_functions = {
#             "get_current_weather": get_current_weather,
#             "turn_on_air_conditioner": turn_on_air_conditioner,
#         }
#         messages.append(response_message)  # extend conversation with assistant's reply


#         # Step 4: send the info for each function call and function response to the model
#         for tool_call in tool_calls:
#             function_name = tool_call.function.name
#             function_to_call = available_functions[function_name]
#             function_args = json.loads(tool_call.function.arguments)
#             function_response = function_to_call(
#                 **function_args
#             )
#             messages.append(
#                 {
#                     "tool_call_id": tool_call.id,
#                     "role": "tool",
#                     "name": function_name,
#                     "content": function_response,
#                 }
#             )  # extend conversation with function response
        
#         # Ask the user for the region if not specified
#         if not any(tool_call.function.name == "get_current_weather" for tool_call in tool_calls):
#             messages.append({"role": "assistant", "content": "Which region do you want to know the weather for?"})
#             second_response = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=messages,
#                 temperature=0.8
#             )
#             return second_response
        
#         second_response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=messages,
#             temperature=0.8
#         )  # get a new response from the model where it can see the function response
#         return second_response

# if __name__ == "__main__":
#     bot_response = run_conversation()
#     print(bot_response.content)
#     # print(bot_response)
#     # if response and response.choices:
#     #     print(response.choices[0].message.content)
