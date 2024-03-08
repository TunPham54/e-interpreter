import threading
#from googletrans import Translator  # Install the googletrans module using pip
import speech_recognition as sr
from openai import OpenAI

def get_user_input(dest_lang):
    r = sr.Recognizer() 
    with sr.Microphone() as source:
        print("Listening...") 
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = r.listen(source)
    try: 
        print("Recognizing...")
        query = r.recognize_google(audio, language = dest_lang)
        print(f"{query}") 
    except Exception: 
        print("Please repeat.....") 
        return "None"
    return query

def translate_to_japanese(prompt, from_lang, to_lang, client):
    # Make a request to the OpenAI API for translation
    chat = f"Translate this piece of text from {from_lang} to {to_lang} (disregard the phonetic transcription): {prompt}"
    response = client.chat.completions.create(model="gpt-4",
    messages = [{"role": "user", "content": chat}])
    return response.choices[0].message.content.strip()

def main():
    dest_lang = input("dest_lang: ")
    to_lang = input("to_lang: ")
    key = open("gpt_api_key", "r").read()
    client = OpenAI(api_key=key)
    while True:
        # Create a thread for the first function
        thread1 = threading.Thread(target=lambda: get_user_input(dest_lang))

        # Create a thread for the second function
        thread2 = threading.Thread(target=lambda: translate_to_japanese(thread1.run(), dest_lang, to_lang, client))
        
        # Start both threads simultaneously
        thread1.start()
        thread2.start()

        # Wait for both threads to finish
        thread1.join()
        thread2.join()

if __name__ == "__main__":
    main()
