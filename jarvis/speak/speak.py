import logging
from time import sleep

import pyttsx3
from utils.logger import setup_logger

engine = pyttsx3.init()  # object creation

logger = logging.getLogger(__name__)

setup_logger(logger)


""" RATE"""

rate = 162
engine.setProperty("rate", 160)  # setting up new voice rate

"""VOLUME"""
volume = 0.8
engine.setProperty("volume", 0.8)  # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty("voices")  # getting details of current voice

# engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty(
    "voice", voices[0].id
)  # changing index, changes voices. 1 for female


def speak(message):
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


# """Saving Voice to a file"""
# # On linux make sure that 'espeak' and 'ffmpeg' are installed
# engine.save_to_file('Hello World', 'test.mp3')
# engine.runAndWait()
