import logging
from time import sleep

import pyttsx3
from gtts import gTTS
from playsound import playsound
from utils.logger import setup_logger
from utils.singleton import SingletonMeta

logger = logging.getLogger(__name__)
setup_logger(logger)


GTTS_ENGINE = "gtts"
PYTTSX3_ENGINE = "pyttsx3"
SPEECH_ENGINE_DEFAULT = GTTS_ENGINE


class TextToSpeach(metaclass=SingletonMeta):

    _data = {}

    RATE = 162
    VOLUME = 0.8
    VOICE_INDEX = 0

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


def speak(message):
    if SPEECH_ENGINE_DEFAULT == GTTS_ENGINE:
        speak_gtts(message)
    else:
        speak_pyttsx3(TextToSpeach.engine(), message)


def speak_gtts(message):
    audio = gTTS(message, tld="com", lang="en")
    audio.save("textaudio.mp3")
    playsound("textaudio.mp3")


def speak_pyttsx3(engine, message):
    if not engine._inLoop:
        engine.say(message)
        logger.info("Not in loop..run and wait")
        engine.runAndWait()
        sleep(2)
        engine.endLoop()
    else:
        logger.info("in loop..stop, run and wait")
        engine.endLoop()
        engine.say(message)
        engine.runAndWait()
        sleep(2)
        engine.endLoop()
