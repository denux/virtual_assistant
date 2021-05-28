import speech_recognition as sr
import pyttsx3


class AudioUtility:
    """
    AudioUtility class includes functions involved with taking input from microphone and providing output as audio.
    """

    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)

    def take_command(self):
        """
        function to interact with microphone of the computer and take command
        :return: the command spoken as string
        """
        try:
            listener = sr.Recognizer()
            with sr.Microphone() as source:
                print('listening...')
                self.talk("listening")
                listener.adjust_for_ambient_noise(source, duration=0.5)
                voice = listener.listen(source,timeout=15)
                command = listener.recognize_google(voice)
                command = command.lower()
                self.talk("command taken")
                return command
        except Exception as e:
            print(e)

    def talk(self, text):
        """
        function to talk back text
        :param text: string to be converted to audio
        """
        self.engine.say(text)
        self.engine.runAndWait()
