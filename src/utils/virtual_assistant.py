import pywhatkit
import datetime
import pyjokes
import random
import json
import pyowm
import re
from utils.audio_utility import AudioUtility
from utils.features import Features
from utils.find_nearest import FindNearest
from dotenv import load_dotenv
import os

load_dotenv()


class VirtualAssistant:
    def __init__(self):
        self.config_json = self.read_config_json(os.getenv("config_json_path", ""))
        self.owm = pyowm.OWM(os.getenv("pyowm_key", ""))
        self.audio = AudioUtility()
        self.feature = Features(self.audio, self.config_json)
        self.find_nearest = FindNearest(self.config_json.get("find_nearest"))

    @staticmethod
    def read_config_json(path):
        """
        function to read config.json file
        :return: dictionary object
        """
        with open(path, "rb") as f:
            config_json = json.load(f)
        return config_json

    def run_elsa(self, command=None):
        """
        main function to call all the features.
        :return: True if we want to exit
        """
        if not command:
            command = self.audio.take_command()
        print("command :", command)
        if not command:
            pass
        elif re.search(r'\b(elsa)\b', command):
            command = command.replace('elsa', '')
            if re.search(r'\b(play)\b', command):
                song = command.split("play")[-1]
                self.audio.talk(random.choice(self.config_json["statements"]["playing"]) + song)
                pywhatkit.playonyt(song)

            elif re.search(r'\b(open)\b', command):
                command = command.split("open")[-1]
                self.feature.open_app(command)

            elif re.search(r'\b(time)\b', command):
                time = datetime.datetime.now().strftime('%I:%M %p')
                self.audio.talk('Current time is ' + time)

            elif re.search(r'\b(joke)\b', command):
                self.audio.talk(pyjokes.get_joke())

            elif "go to sleep" in command:
                self.audio.talk(random.choice(self.config_json["statements"]["sleep"]))
                return True

            elif re.search(r'\b(temperature)\b', command):
                observation = self.owm.weather_manager().weather_at_place("New Delhi").weather.temperature('celsius')[
                    "temp"]
                self.audio.talk(str(observation) + " degree celsius")

            elif re.search(r'\b(nearest)\b', command):
                entity = self.find_nearest.get_entity(command)
                list_places = self.find_nearest.get_search_results(entity)
                if len(list_places) != 0:
                    self.audio.talk("These are the nearest {} from your current location".format(entity))
                    for i in list_places:
                        print(i)
                        self.audio.talk(i)
                else:
                    self.audio.talk("Sorry no search results found. Check command and try again.")

            elif re.search(r'\b(cases)\b', command) or re.search(r'\b(covid)\b', command):
                self.audio.talk("for which state you want covid report")
                command = self.audio.take_command()
                if not command or command not in self.config_json["states"]:
                    self.audio.talk(random.choice(self.config_json["statements"]["understand"]))
                else:
                    self.feature.get_covid_report(command)

            elif (re.search(r'\b(who)\b', command) or re.search(r'\b(what)\b', command)) \
                    and re.search(r'\b(is)\b', command):
                self.feature.search_online(command)

            elif re.search(r'\b(date)\b', command):
                self.audio.talk(random.choice(self.config_json["statements"]["date"]))

            else:
                self.audio.talk(random.choice(self.config_json["statements"]["command_not_found"]))
        else:
            self.audio.talk("Unrecognized command")

    def start_assistant(self, command=None):
        self.audio.talk(self.feature.get_greeting())
        while True:
            if self.run_elsa(command):
                break
            elif command:
                break
        self.audio.talk("Thank you")
