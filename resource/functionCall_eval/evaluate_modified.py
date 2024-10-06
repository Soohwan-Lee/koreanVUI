#!/usr/bin/env python3

import os
import click
from src import utils
from src.payload_creator import PayloadCreatorFactory
from src.response_handler import ResponseHandler
from src.evaluation_handler import EvaluationHandler

REPO_NAME = "FunctionChat-Bench"
CUR_PATH = os.path.abspath(__file__)
REPO_PATH = f"{CUR_PATH.split(REPO_NAME)[0]}{REPO_NAME}"

# Default values
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_INPUT_PATH = "./data/FunctionChat-Dialog.jsonl"
DEFAULT_SYSTEM_PROMPT_PATH = "./data/system_prompt.txt"
DEFAULT_TEMPERATURE = 0.1
DEFAULT_API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL_PATH = None
DEFAULT_GCLOUD_PROJECT_ID = None
DEFAULT_GCLOUD_LOCATION = None

def run_evaluation():
    # dialog / singlecall
    eval_type = "dialog"
    TEST_PREFIX = f'FunctionChat-{eval_type.capitalize()}'

    print(f"[[{DEFAULT_MODEL} {TEST_PREFIX} evaluate start]]")
    utils.create_directory(f'{REPO_PATH}/output/')

    request_file_path = f'{REPO_PATH}/output/{TEST_PREFIX}.input.jsonl'
    predict_file_path = f'{REPO_PATH}/output/{TEST_PREFIX}.{DEFAULT_MODEL}.output.jsonl'
    eval_file_path = f'{REPO_PATH}/output/{TEST_PREFIX}.{DEFAULT_MODEL}.eval.jsonl'
    eval_log_file_path = f'{REPO_PATH}/output/{TEST_PREFIX}.{DEFAULT_MODEL}.eval_report.tsv'

    api_request_list = PayloadCreatorFactory.get_payload_creator(
        eval_type, DEFAULT_TEMPERATURE, DEFAULT_SYSTEM_PROMPT_PATH
    ).create_payload(
        input_file_path=DEFAULT_INPUT_PATH, request_file_path=request_file_path, reset=False)
    
    api_response_list = ResponseHandler(
        DEFAULT_MODEL, DEFAULT_API_KEY, DEFAULT_BASE_URL, DEFAULT_MODEL_PATH,
        DEFAULT_GCLOUD_PROJECT_ID, DEFAULT_GCLOUD_LOCATION
    ).fetch_and_save(
        api_request_list, predict_file_path, reset=False, sample=False, debug=False
    )
    
    EvaluationHandler(eval_type).evaluate(
        api_request_list, api_response_list,
        eval_file_path, eval_log_file_path,
        reset=False, sample=False, debug=False
    )

if __name__ == '__main__':
    run_evaluation()