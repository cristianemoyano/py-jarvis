import logging
from abc import ABC, abstractmethod
from time import sleep

import pyttsx3
from gtts import gTTS
from playsound import playsound
from settings import SETTINGS

logger = logging.getLogger(__name__)


class SpeakStrategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def speak(self, message):
        pass


class SpeakAPI:
    """
    The SpeakAPI defines the interface of interest to clients.
    """

    def __init__(self, strategy):
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        """
        SpeakAPI allows replacing a Strategy object at runtime.
        """
        self._strategy = strategy

    def speak(self, message):
        self._strategy.speak(message)


class GTTSEngineStrategy(SpeakStrategy):
    def speak(self, message):
        audio = gTTS(message, tld=SETTINGS.GTTS_TLD, lang=SETTINGS.GTTS_LANG)
        audio.save(SETTINGS.GTTS_AUDIO_FILENAME)
        playsound(SETTINGS.GTTS_AUDIO_FILENAME)


class Pyttsx3EngineStrategy(SpeakStrategy):
    _data = {}

    RATE = SETTINGS.PYTTSX3_RATE
    VOLUME = SETTINGS.PYTTSX3_VOLUME
    VOICE_INDEX = SETTINGS.PYTTSX3_VOICE_INDEX

    @classmethod
    def engine(cls):
        cls.setup_engine()
        return cls._data["engine"]

    @classmethod
    def setup_engine(cls):
        if not cls._data:
            engine = pyttsx3.init()  # object creation
            engine.setProperty("rate", cls.RATE)  # setting up new voice rate
            engine.setProperty(
                "volume", cls.VOLUME
            )  # setting up volume level  between 0 and 1
            voices = engine.getProperty("voices")  # getting details of current voice
            # engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
            engine.setProperty(
                "voice", voices[cls.VOICE_INDEX].id
            )  # changing index, changes voices. 1 for female
            cls._data["engine"] = engine

    def speak(self, message):
        if not self.engine()._inLoop:
            self.engine().say(message)
            logger.info("Not in loop..run and wait")
            self.engine().runAndWait()
            sleep(2)
            self.engine().endLoop()
        else:
            logger.info("in loop..stop, run and wait")
            self.engine().endLoop()
            self.engine().say(message)
            self.engine().runAndWait()
            sleep(2)
            self.engine().endLoop()


def get_speak_strategy_instance(strategy_code):
    SPEECH_ENGINE_MAP = {
        SETTINGS.GTTS_ENGINE: GTTSEngineStrategy,
        SETTINGS.PYTTSX3_ENGINE: Pyttsx3EngineStrategy,
    }
    return SPEECH_ENGINE_MAP[strategy_code]()


def speak(message):
    api = SpeakAPI(get_speak_strategy_instance(SETTINGS.SPEECH_ENGINE_DEFAULT))
    api.speak(message)
