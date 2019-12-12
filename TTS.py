import pyttsx3

def init_engine():

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 200)     # setting up new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    #engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
    return engine

def read(engine, text):
    engine.say(text)
    engine.runAndWait()
