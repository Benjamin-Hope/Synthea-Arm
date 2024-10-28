import speech_recognition as sr


class SpeechRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def recognize(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        try:
            self.text = self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            self.text = "Sorry, I could not understand what you said"
        except sr.RequestError:
            self.text = "Sorry, my speech service is down"
        return self.text


## Test
'''
micro = SpeechRecognition()
result = micro.recognize()

print(result)'''