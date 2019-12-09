# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 20:04:08 2019

@author: Mario Acera
"""
#pip install pyttsx3
import pyttsx3
engine = pyttsx3.init()
a='You have and appointment on the same day, one HOUR before'
b='Would you want to set this appointment a hour later?'

rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 130)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')  
print(voices)     #getting details of current voice
engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
#engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female



engine.say(a)
engine.say(b)
engine.runAndWait()