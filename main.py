from openai import OpenAI
from google import genai
import os
from dotenv import load_dotenv
from actions import get_response_time
from prompts import system_prompt
from json_helpers import extract_json

# Load environment variables
load_dotenv()

# Create an instance of the OpenAI class
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_text_with_conversation_OPENAI(messages, model = "gpt-3.5-turbo"):
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages
        )
    return response.choices[0].message.content


def generate_text_with_conversation_GEMINI(messages, model="gemini-2.5-flash"):
    response = client.models.generate_content(
                model=model,
                contents=messages
                )
    return response.text

# Available actions are defined in actions.py
available_actions = {
    "get_response_time": get_response_time
}

user_prompt = "What is the response time for learnwithhasan.com?"

messages = [
    {"role": "system", "content": system_prompt}, # system prompt for the AI agent imported from prompts.py
    {"role": "user", "content": user_prompt}
]

# translate the loop to into python loop to wroks for the Agent properly

turn_count = 1
max_turns = 5


while turn_count < max_turns:
    print (f"Loop: {turn_count}")
    print("----------------------")
    turn_count += 1

    # response = generate_text_with_conversation_OPENAI(messages, model="gpt-3.5-turbo")
    response=generate_text_with_conversation_GEMINI(messages, model="gemini-2.5-flash")

    print(response)

    json_function = extract_json(response)

    if json_function:
            function_name = json_function[0]['function_name']
            function_parms = json_function[0]['function_parms']
            if function_name not in available_actions:
                raise Exception(f"Unknown action: {function_name}: {function_parms}")
            print(f" -- running {function_name} {function_parms}")
            action_function = available_actions[function_name]
            #call the function
            result = action_function(**function_parms)
            function_result_message = f"Action_Response: {result}"
            messages.append({"role": "user", "content": function_result_message})
            print(function_result_message)
    else:
         break