from openai import OpenAI
import json

# YOUR_API_KEY
client = OpenAI(api_key="YOUR_API_KEY")

def text_generate_GPT(messages, tools):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    response_message = response.choices[0].message
    messages.append(response_message)  # Extend conversation with assistant's reply
    return messages, response_message.tool_calls, response_message.content

def end_conversation():
    """Function to signify the end of the conversation with a nice message."""
    return json.dumps({"message": "Thank you for chatting with me! Have a wonderful day!"})

def main():
    personality = "You are a social robot for the elderly and your name is LEMMY. You were created at UNIST. You respond in short, friendly sentences that the elderly can understand."
    messages = [{"role": "system", "content": f"{personality}"}]
    tools = [
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
    dialogueEnd = False
    while not dialogueEnd:
        print("="*30)
        user_input = input('User: ')
        messages.append({"role": "user", "content": f"{user_input}"})
        messages, tool_calls, lemmy_response = text_generate_GPT(messages, tools)
        
        # Print LEMMY's response here
        if lemmy_response:
            print(f'LEMMY: {lemmy_response}')
        
        if tool_calls:
            available_functions = {
                "end_conversation": end_conversation,
            }
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_response = function_to_call()
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            # Append the function response and user instruction
            final_message_content = json.loads(function_response)["message"]
            messages.append({"role": "assistant", "content": final_message_content})
            messages.append({"role": "user", "content": "Please end the conversation and say something nice."})
            
            # Get a new response from the model where it can see the function response
            final_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )
            final_message = final_response.choices[0].message.content
            if final_message:  # Only print if there's a message
                print(f'LEMMY: {final_message}')
            dialogueEnd = True
            return
        print(f"Dialogue End: {dialogueEnd}")

if __name__ == "__main__":
    main()