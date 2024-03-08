# Importing necessary modules required 
from playsound import playsound 
import speech_recognition as sr 
#from googletrans import Translator 
from gtts import gTTS 
import os
from openai import OpenAI 
from elevenlabs import set_api_key, generate, play
from pathlib import Path
import threading
import queue

def gpt_chat_box(from_lang, to_lang, client, prompt):
    # Make a request to the OpenAI API for translation
    chat = f"Translate this piece of text from {from_lang} to {to_lang} (disregard the phonetic transcription): {prompt}"
    response = client.chat.completions.create(model="gpt-4",
    messages = [{"role": "user", "content": chat}])
    return response.choices[0].message.content.strip()
    # Extract the translated text from the API response

def detect_lang(dic, dest_lang):
     lang = dest_lang.capitalize()
     if lang in dic:
         lang = dic[dic.index(lang)-1]
         return lang
     else:
         print("The language is not available for translation")
         return False

# Capture Voice through microphone 
def takecommand(dest_lang):
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
        print("Please repeat...") 
        return "None"
    return query 

def tts(prompt):
 key = open("11_api_key", "r").read()
 set_api_key(f"{key}")
 audio = generate(
  text=prompt,
  voice="Knightley",
  model="eleven_multilingual_v2"
 )
 play(audio) 

def play_sound():
   playsound("speech.mp3")

def print_trans(text):
   print(text)
   
def input_stt(from_lang, input_queue):
    count = 0
    query = takecommand(from_lang)
    while (query == "None") and count < 2:
        count += 1
        query = takecommand(from_lang) 
    input_queue.put(query)    

def output_tts_gpt(client, text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model = 'tts-1',
        voice = 'nova',
        input = text
    )
    response.stream_to_file(speech_file_path)
    thread1 = threading.Thread(target = play_sound)
    thread2 = threading.Thread(target = print_trans, args=(text,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    os.remove('speech.mp3')

def output_tts_11(text):
    thread1 = threading.Thread(target = tts, args=(text,))
    thread2 = threading.Thread(target = print_trans, args=(text,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()    

def output_gg_trans(text, to_lang):
     speak = gTTS(text = text, lang = to_lang, tld='com', slow = False)
     speak.save("trans_voice.mp3")
     playsound("trans_voice.mp3")
     os.remove("trans_voice.mp3")

def main():
 key = open("gpt_api_key", "r").read()
 client = OpenAI(api_key=key)
 result_queue = queue.Queue()
 count = 0
 dic = ('af', 'Afrikaans', 'ar', 'Arabic', 'bg', 'Bulgarian', 
        'bn', 'Bengali', 'bs', 'Bosnian', 'ca', 'Catalan', 
        'cs', 'Czech', 'da', 'Danish', 'de', 'German', 
        'el', 'Greek', 'en', 'English', 'es', 'Spanish', 
        'et', 'Estonian', 'fi', 'Finnish', 'fr', 'French', 
        'gu', 'Gujarati', 'hi', 'Hindi', 'hr', 'Croatian', 
        'hu', 'Hungarian', 'id', 'Indonesian', 'is', 'Icelandic', 
        'it', 'Italian', 'iw', 'Hebrew', 'ja', 'Japanese', 
        'jw', 'Javanese', 'km', 'Khmer', 'kn', 'Kannada', 
        'ko', 'Korean', 'la', 'Latin', 'lv', 'Latvian', 
        'ml', 'Malayalam', 'mr', 'Marathi', 'ms', 'Malay', 
        'my', 'Myanmar (Burmese)', 'ne', 'Nepali', 'nl', 'Dutch', 
        'no', 'Norwegian', 'pl', 'Polish', 'pt', 'Portuguese', 
        'ro', 'Romanian', 'ru', 'Russian', 'si', 'Sinhala', 
        'sk', 'Slovak', 'sq', 'Albanian', 'sr', 'Serbian', 
        'su', 'Sundanese', 'sv', 'Swedish', 'sw', 'Swahili', 
        'ta', 'Tamil', 'te', 'Telugu', 'th', 'Thai', 
        'tl', 'Filipino', 'tr', 'Turkish', 'uk', 'Ukrainian', 
        'ur', 'Urdu', 'vi', 'Vietnamese', 'zh-CN', 'Chinese', 
        'zh-TW', 'Taiwan')
 eleven_dic = ('English', 'Japanese', 'Chinese', 
           'Taiwan', 'German', 'Hindi', 
           'French', 'Korean', 'Portuguese', 
           'Italian', 'Spanish', 'Indonesian', 
           'Dutch', 'Turkish', 'Filipino',
           'Polish', 'Swedish', 'Bulgarian'
           'Romanian', 'Arabic', 'Czech', 
           'Greek', 'Finnish', 'Croatian',
           'Malay', 'Slovak', 'Danish', 
           'Tamil', 'Ukranian')
 gpt_dic = ('Afrikaans', 'Arabic', 'Armenian', 
            'Azerbaijani', 'Belarusian', 'Bosnian', 
            'Bulgarian', 'Catalan', 'Chinese', 
            'Croatian', 'Czech', 'Danish', 
            'Dutch', 'English', 'Estonian', 
            'Finnish', 'French', 'Galician', 
            'German', 'Greek', 'Hebrew', 
            'Hindi', 'Hungarian', 'Icelandic', 
            'Indonesian', 'Italian', 'Japanese', 
            'Kannada', 'Kazakh', 'Korean', 
            'Latvian', 'Lithuanian', 'Macedonian', 
            'Malay', 'Marathi', 'Maori', 
            'Nepali', 'Norwegian', 'Persian', 
            'Polish', 'Portuguese', 'Romanian',
            'Russian', 'Serbian', 'Slovak', 
            'Slovenian', 'Spanish', 'Swahili', 
            'Swedish', 'Tagalog', 'Tamil', 
            'Thai', 'Turkish', 'Ukrainian', 
            'Urdu', 'Vietnamese', 'Welsh')     
 print("Language Translation:")
 from_lang_in = input("From: ")
 from_lang = detect_lang(dic, from_lang_in)
 while not from_lang:
     from_lang_in = input("From: ")
     from_lang = detect_lang(dic, from_lang_in)
 print("\u2193")
 to_lang_in = input("To: ")
 to_lang = detect_lang(dic, to_lang_in)
 while not to_lang:
     to_lang_in = input("To: ")
     to_lang = detect_lang(dic, to_lang_in)     
 #Print received text
 query = takecommand(from_lang)
 while (query == "None") and count <= 3:
     count += 1
     query = takecommand(from_lang)
     if query != "None":
         break
     else: 
         return     
 while True and query != "None": 
    #query = input_stt(from_lang)
    text = gpt_chat_box(from_lang_in, to_lang_in, client, query)
    #thread2 = threading.Thread(target = gpt_chat_box, args = (result_queue, from_lang_in, to_lang_in, client))
    #thread2.start()
    #thread2.join()
    print("\u2193")
    if to_lang_in.capitalize() in gpt_dic: 
        #output_tts_gpt(client, text)
        thread2 = threading.Thread(target = output_tts_gpt, args=(client, text,))
        #thread2 = threading.Thread(target = print_trans, args=(text,))
        thread1 = threading.Thread(target = input_stt, args = (from_lang, result_queue,))
        thread2.start()
        thread2.join()
        thread1.start()     
        thread1.join()
        query = result_queue.get()
        if query == "None":
            return
    elif to_lang_in.capitalize() in eleven_dic:
        thread1 = threading.Thread(target = output_tts_11, args = (text))
        thread2 = threading.Thread(target = input_stt, args = (from_lang, result_queue,))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
        query = result_queue.get()
        if query == "None":
            return        
    else:
        thread2 = threading.Thread(target = input_stt, args = (from_lang, result_queue,))
        thread1 = threading.Thread(target = output_gg_trans, args = (text, to_lang,))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
        query = result_queue.get()
        if query == "None":
            return        
if __name__ == "__main__":
    main()

