from openai import OpenAI

key = open("gpt_api_key", "r").read()
client = OpenAI(api_key=key)

def gpt_chat_box(prompt):

    # Make a request to the OpenAI API for translation
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages = [{"role": "user", "content": prompt}])
    
    # Extract the translated text from the API response
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "end"]:
            break
        response = gpt_chat_box(user_input)
        print("GPT 3.5: ", response)