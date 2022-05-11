import logging
import time

import speech_recognition as sr

# Example:
# https://github.com/Uberi/speech_recognition/tree/master/examples


logger = logging.getLogger(__name__)


def callback(recognizer, audio):
    # this is called from the background thread
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        logger.info(
            "Google Speech Recognition thinks you said: "
            + recognizer.recognize_google(audio)
        )
    except sr.UnknownValueError:
        logger.info("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        logger.info(
            f"Could not request results from Google Speech Recognition service; {e}"
        )


r = sr.Recognizer()
m = sr.Microphone(0)
with m as source:
    logger.info("Calibrating..")
    r.adjust_for_ambient_noise(
        source, duration=2
    )  # we only need to calibrate once, before we start listening

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
