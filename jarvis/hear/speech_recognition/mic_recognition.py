import logging
import time

import speech_recognition as sr
from utils.logger import setup_logger

# Example:
# https://github.com/Uberi/speech_recognition/tree/master/examples


logger = logging.getLogger(__name__)

setup_logger(logger)

r = sr.Recognizer()
m = sr.Microphone(0)
with m as source:
    logger.info("Calibrating..")
    r.adjust_for_ambient_noise(
        source, duration=2
    )  # we only need to calibrate once, before we start listening


def listen(callback):
    logger.info("listening in the background ..")
    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback)
    # `stop_listening` is now a function that, when called, stops background listening

    logger.info("Do something else..")
    # do some unrelated computations for 5 seconds
    time.sleep(
        60
    )  # we're still listening even though the main thread is doing other things

    logger.info("Stop listening..")
    # calling this function requests that the background listener stop listening
    stop_listening(wait_for_stop=False)

    logger.info("End..")
    # do some more unrelated things
    # we're not listening anymore,
    # even though the background thread might still be running for a second
    # or two while cleaning up and stopping
