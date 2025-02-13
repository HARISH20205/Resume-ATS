import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv()



sys_instruct="Provide the output in JSON format where the key is the topic and the value is a list of relevant contents. Ensure the response is clear, user friendly, structured."
def get_response(prompt,task):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=task+sys_instruct,response_mime_type='application/json',temperature=0.6),
        contents=prompt
    )
    # print(response.text)
    return response.text

# get_response("What is AI?","explain the given prompt")