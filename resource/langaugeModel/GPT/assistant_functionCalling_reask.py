import os
import json
from openai import OpenAI
import time

# Set your OpenAI API key 'YOUR_API_KEY'
api_key = "YOUR_API_KEY"

# Create a client object to use the OpenAI API.
client = OpenAI(api_key=api_key)

# Function for getting weather information (Test)
def get_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "울산" in location.lower():
        print("***Function Calling***: Ulsan's Weather!")
        return json.dumps({"location": "울산", "temperature": "25", "unit": unit})
    elif "서울" in location.lower():
        return json.dumps({"location": "서울", "temperature": "27", "unit": unit})
    elif "창원" in location.lower():
        return json.dumps({"location": "창원", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

# Function to display JSON
def show_json(obj):
    print(json.dumps(obj, indent=2))

# Function to create a new thread
def create_new_thread():
    """
    Creates a new conversation thread.
    """
    thread = client.beta.threads.create()
    return thread

# Function to wait for the run to complete
def wait_on_run(run, thread_id):
    """
    Waits for the run to complete by polling its status.
    """
    while run.status == "queued" or run.status == "in_progress":
        # 3-3. 실행 상태를 최신 정보로 업데이트합니다.
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

# Function to submit a message in the thread
def submit_message(assistant_id, thread_id, user_message):
    """
    Sends a message in the specified thread and starts a run.
    """
    # 3-1. 스레드에 종속된 메시지를 '추가' 합니다.
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=user_message
    )
    # 3-2. 스레드를 실행합니다.
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    return run

# Function to get the response messages from the thread
def get_response(thread_id):
    """
    Retrieves the messages from the specified thread.
    """
    return client.beta.threads.messages.list(thread_id=thread_id, order="asc")

# Function to print messages from the response
def print_message(response):
    """
    Prints the messages from the response.
    """
    for res in response.data:
        print(f"[{res.role.upper()}]\n{res.content[0].text.value}\n")

# Function to handle a user's message and get a response
def ask(assistant_id, thread_id, user_message):
    """
    Submits a user's message and retrieves the assistant's response.
    """
    run = submit_message(
        assistant_id,
        thread_id,
        user_message,
    )
    # 실행이 완료될 때까지 대기합니다.
    run = wait_on_run(run, thread_id)
    handle_function_calls(run, thread_id)
    print_message(get_response(thread_id))
    return run

# Function to handle function calls within a run
def handle_function_calls(run, thread_id):
    """
    Handles function calls required by the run.
    """
    if run.required_action and hasattr(run.required_action, 'submit_tool_outputs'):
        tool_outputs = []
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            # Parse the JSON string in the function arguments
            function_args = json.loads(tool.function.arguments)
            if tool.function.name == "get_weather":
                location = function_args.get("location")
                if not location or location == "unknown":
                    # If location is not provided, ask the user for the location
                    client.beta.threads.messages.create(
                        thread_id=thread_id, role="assistant", content="어느 지역의 날씨를 원하시나요?"
                    )
                else:
                    output = get_weather(location)
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": output
                    })

        if tool_outputs:
            try:
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
            except Exception as e:
                print("Failed to submit tool outputs:", e)
    return run

# Main function to facilitate a multi-turn conversation with the assistant
def main():
    """
    Main function to facilitate a multi-turn conversation with the assistant.
    """
    # Create a new assistant
    ASSISTANT_ID = "asst_4Eg0Fv97rAVVnwmnpuXFpCOC"

    # Create a new thread
    thread = create_new_thread()
    show_json(thread.model_dump())  # Use model_dump to get serializable data
    THREAD_ID = thread.id

    user_input = ""
    while user_input.lower() != "exit":
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        run = ask(ASSISTANT_ID, THREAD_ID, user_input)
        # show_json(run.model_dump())  # Use model_dump to get serializable data

if __name__ == "__main__":
    main()
