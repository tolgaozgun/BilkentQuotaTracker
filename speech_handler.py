import pyttsx3

class SpeechHandler:
    def __init__(self, voice: str="male", rate: int=200, volume: float=1.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', voice)
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def say(self, message: str):
        self.engine.say(message)
        self.engine.runAndWait()