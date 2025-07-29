import os
from dotenv import load_dotenv
from google import genai



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    model  = "gemini-2.0-flash-001"
    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    resp = client.models.generate_content(model=model, contents=prompt)

    print(f"Response: {resp.text}")
    print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
