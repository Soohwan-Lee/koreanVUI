import os
import google.cloud.dialogflow_v2 as dialogflow

file_path = './resource/intentRecognition/'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = file_path + 'lemme2-hvvh-93b9c4459fd3.json'   #Private Key
DIALOGFLOW_PROJECT_ID = 'lemme2-hvvh'   #Project ID
DIALOGFLOW_LANGUAGE_CODE = 'ko'
SESSION_ID = 'me'

session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

# our_query = "날씨 알려줘"
while True:
    print("=======================")
    our_query = input("Talk to Lemmy!: ")

    our_input = dialogflow.types.TextInput(text=our_query, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query = dialogflow.types.QueryInput(text=our_input)
    response = session_client.detect_intent(session=session, query_input=query)

    print("Our text:", response.query_result.query_text)
    print("Dialogflow's response:", response.query_result.fulfillment_text)
    print("Dialogflow's intent:", response.query_result.intent.display_name)