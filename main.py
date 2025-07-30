import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    model  = "gemini-2.0-flash-001"
    messages = []

    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        messages = [
            types.Content(role="user", parts=[types.Part(text=prompt)]),
        ]

    else:
        print("Error: no prompt provided.")
        sys.exit(1)

    resp = client.models.generate_content(model=model, contents=messages)


    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"User prompt: {resp.text}")
        print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
