import speech_recognition as sr
from openai import OpenAI
key = open("gpt_api_key", "r").read()
client = OpenAI(api_key=key)

def continuous_speech_recognition():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        while True:
            try:
                audio = recognizer.listen(source, timeout = None)
                recognizer.adjust_for_ambient_noise(source)
                #recognized_text = recognizer.recognize_google(audio)
                recognized_text = client.audio.transcriptions.create(
                    model = 'whisper-1',
                    file = audio,
                    response_format= "text"
                )

                if recognized_text:
                    print("You said:", recognized_text)

            except sr.UnknownValueError:
                print("Could not understand audio")

            except sr.RequestError as e:
                print("Error with the speech recognition service; {0}".format(e))

if __name__ == "__main__":
    continuous_speech_recognition()

