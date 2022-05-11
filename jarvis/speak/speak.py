import pyttsx3

engine = pyttsx3.init()  # object creation

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

engine.say("Hey there! My name is Jarvis, but you can call me J")
engine.runAndWait()
engine.stop()

# """Saving Voice to a file"""
# # On linux make sure that 'espeak' and 'ffmpeg' are installed
# engine.save_to_file('Hello World', 'test.mp3')
# engine.runAndWait()
