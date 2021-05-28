import requests
import subprocess
import wikipedia
import random
import datetime as dt


class Features:
    """
    This class contains all the current features that are part of the Virtual Assistant.
    Various capabilities including retrieval of Covid19 reports, opening application and web search, are provided here.
    """

    def __init__(self, obj_aud, config_json):
        self.covid_json = requests.get(config_json.get("covid_api")).json()
        self.obj_aud = obj_aud
        self.config_json = config_json

    def get_covid_report(self, state):
        """
        function to talk about the covid reports of input state
        :param state: name of state as string
        :return: covid report as voice
        """
        for i in self.covid_json["statewise"]:
            if i["state"].lower() == state.lower():
                self.obj_aud.talk("confirmed " + i["confirmed"])
                self.obj_aud.talk("active " + i["active"])
                self.obj_aud.talk("deaths " + i["deaths"])
                self.obj_aud.talk("recovered " + i["recovered"])

    def open_app(self, p):
        """
        function to open a specific application installed on the computer
        :param p: program name as a string to be opened
        """
        p = p.upper()
        if ("GOOGLE" in p) or ("SEARCH" in p) or ("WEB BROWSER" in p) or ("CHROME" in p):
            self.obj_aud.talk("Opening")
            self.obj_aud.talk("GOOGLE CHROME")
            subprocess.call(self.config_json["application_paths"]["chrome"])

        elif ("NOTE" in p) or ("NOTES" in p) or ("NOTEPAD" in p) or ("EDITOR" in p):
            self.obj_aud.talk("Opening")
            self.obj_aud.talk("NOTEPAD")
            subprocess.call(self.config_json["application_paths"]["notepad"])

        elif ("VLCPLAYER" in p) or ("PLAYER" in p) or ("VIDEO PLAYER" in p):
            self.obj_aud.talk("Opening")
            self.obj_aud.talk("VLC PLAYER")
            subprocess.call(self.config_json["application_paths"]["vlc"])

        else:
            self.obj_aud.talk(p)
            self.obj_aud.talk("not found on this computer")

    @staticmethod
    def get_greeting():
        current_hr = dt.datetime.now().time().hour
        if 0 <= current_hr <= 11:
            return "good morning"
        elif 12 <= current_hr <= 15:
            return "good afternoon"
        elif 16 <= current_hr <= 20:
            return "good evening"
        else:
            return "good night"

    def search_online(self, command):
        """
        function to find web search results of a specific string
        :param command: string to be searched online
        """
        search_term = command.split("is")[-1]
        self.obj_aud.talk(random.choice(self.config_json["statements"]["searching"]) + search_term)
        print("searching", search_term)
        try:
            info = wikipedia.summary(search_term, sentences=3)
            self.obj_aud.talk(info)
        except wikipedia.DisambiguationError as e:
            self.obj_aud.talk("Found multiple result online for what you said.")
            self.obj_aud.talk("The top results includes the following, please select number for one of these")
            options = list(e.options)
            for choice, term in enumerate(options):
                choice = choice + 1
                if choice == 6:
                    break
                self.obj_aud.talk(str(choice) + "  " + term)
            command_choice = self.obj_aud.take_command()
            try:
                if not command_choice or int(command_choice) not in range(1, 6):
                    self.obj_aud.talk(random.choice(self.config_json["statements"]["choice_not_found"]))
                else:
                    p = wikipedia.summary(options[int(command_choice)], sentences=3)
                    self.obj_aud.talk(p)
            except (ValueError, Exception):
                self.obj_aud.talk(random.choice(self.config_json["statements"]["choice_not_found"]))
