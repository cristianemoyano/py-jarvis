import logging
import time

from hear.speech_recognition.mic_recognition import listen
from speak.speak import speak
from speech_recognition import RequestError, UnknownValueError
from utils.logger import setup_logger

logger = logging.getLogger(__name__)

setup_logger(logger)


def callback(recognizer, audio):
    # this is called from the background thread
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text = recognizer.recognize_google(audio)
        logger.info(text)
        speak(text)
    except UnknownValueError:
        logger.error("Google Speech Recognition could not understand audio..")
        speak("Sorry, can you repeat it again?")
    except RequestError as e:
        logger.error(
            f"Could not request results from Google Speech Recognition service; {e}"
        )


stop_listening = listen(callback)

# we're still listening even though the main thread is doing other things
time.sleep(60)

logger.info("Stop listening..")
# calling this function requests that the background listener stop listening
stop_listening(wait_for_stop=False)
logger.info("Bye.")
