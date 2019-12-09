#Speech recognition
import speech_recognition as sr
import spacy
from spacy import displacy
from pathlib import Path

#TIME
from datetime import datetime
from datetime import timedelta
#To take away the st, nd, th...
import re
#To count how many : in time
from collections import Counter

def speech_recognition():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
        text_speech=r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return text_speech

def parsing(text_speech):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text_speech)

    #POS: The simple part-of-speech tag.
    #Tag: The detailed part-of-speech tag.
    list_tokens=[("Tokens", "Lemma", "Pos", "Dependencies", "Tags")]
    list_ent=[]
    #print(list_tokens)
    for token in doc:
        list1=[]
       # print(token.text, token.pos_, token.dep_)
        list1.append(token.text)
        #Reducing down words to their truly roots. Lemmatization
        list1.append(token.lemma_)
        list1.append(token.pos_)
        list1.append(token.dep_)
        list1.append(token.tag_)
        list_tokens.append(list1)

    for ent in doc.ents:
        #For entities
        list2=[]
        list2.append(ent.text)
        list2.append(ent.label_)
        list_ent.append(list2)
        #print(ent.text, ent.label_)

    #print_list_tokens(list_tokens)

    return list_tokens, list_ent

def print_list_tokens(list_tokens):
    for Text, Lemma, Position, Tag, Dependency in list_tokens:
        print(f"{Text:{20}} {Lemma:{20}} {Position:{20}} {Tag:{20}} {Dependency:{20}}")

#1 FIRST STATE:  verbs like ADD, CANCEL, INFO
def searching_verb(list_of_tokens):
    cnt=0
    idx = None
    verbs_tokens=[]
    for item in list_of_tokens:
        #Add or delete can be written with another verb that can be ROOT, therefore we take into account 'xcomp' as: I want to add an appointment.
        if item[-2]=='xcomp' or  item[-2]=='ROOT'  and item[-3] in ('VERB'):
            #print(item[-2], item[-3])
            idx = cnt
            verbs_tokens.append(item)
            cnt+=1
    #Number to return the corresponding row of the proper token. Watch out cnt+=1
    if len(verbs_tokens) > 0:
        return verbs_tokens[idx]
    else:
        return ""
        #print("You should tell me what you want to do")

#2 SECOND STATE: dates like 25th December, next Monday etc (IN DEVELOPMENT)
def searching_date(list_of_tokens):
    #In case we have more entities we are picking only DATE! For the next states we will pick "TIME" or cardinal.
    weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    month_list=['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
    for text,ent in list_of_tokens:
        #We take into account only the DATE entity
        if ent=="DATE":
            text_split=text.split()
            #Today's Date
            now = datetime.now()
            for n in text_split:
                #We have to take into account different inputs regarding dates in english.
                #CASE 1: On Monday, On Tuesday
                if n in weekDays:

                    #The number of the week to make the loop, [0,6]
                    index_week=weekDays.index(n)
                    #Today's number of the week
                    week_now=now.weekday()
                    #LOOP--> Example (today 4 and appointment 2 (Wednesday)= 5,6,0,1,2= 5 days)
                    find=True
                    cont=week_now
                    d=0
                    while find:
                        #TO ADD A COUNTER TO COUNT FROM TODAY TO THE DAY THAT HAS BEEN SAID
                        for i in range(cont,7):
                            if i==index_week:
                                find=False
                                break
                            elif i==6:
                                cont=0
                            d+=1
                    d=d+1
                    print("The number of days for next appointment is:  %d" % d)
                    #We sum up the days until next appointment to the actual date
                    sum_day=timedelta(days=d)
                    new_date=now+sum_day
                    #We put it in the format we want.
                    date_output=datetime.strftime(new_date, '%d/%m/%Y')
                if n in month_list:
                    #To take away the st, rd, th, and nd
                    date_refined1=re.sub(r'(\d)(st|nd|rd|th)', r'\1', text)
                    #To take away dates with of, in order to be introduced in datetime(year,month,day)
                    date_refined2=date_refined1.replace('of','')
                    date_intro=date_refined2.split()
                    index_month=month_list.index(date_intro[1])+1
                    #CASE 2: 25th December
                    if "20" not in date_intro[-1]:
                        date_current_year=datetime(2019, index_month, int(date_intro[0]), 0, 0)
                        date_output=datetime.strftime(date_current_year, '%d/%m/%Y')
                    #CASE 3: 25th of February 2020
                    else:
                        date_proposed_year=datetime(int(date_intro[-1]), index_month, int(date_intro[0]), 0, 0)
                        date_output=datetime.strftime(date_proposed_year, '%d/%m/%Y')
                #CASE 4 TOMORROW
                if n=="tomorrow":
                    tomorrow_days=timedelta(days=1)
                    tomorrow=now+tomorrow_days
                    date_output=datetime.strftime(tomorrow, '%d/%m/%Y')
                #CASE 5 TODAY
                if n=="today":
                    date_output=datetime.strftime(now, '%d/%m/%Y')


    return date_output

def searching_time(list_of_tokens):
    for text,ent in list_of_tokens:
        #We take into account only the DATE entity
        if ent=="TIME":
            count = Counter(text)
            x=count[':']
            time_refined1=text.replace('.','')
            format = '%I:%M %p'
            #Primera casuistica, 2:30 pm to 3:30 pm
            if x==2:
                from_time=time_refined1[0:7]
                to_time=time_refined1[-7:]
                # print(from_time)
                # print(to_time)
                my_timestrp_from = datetime.strptime(from_time, format)
                my_timestrp_to = datetime.strptime(to_time, format)
                str_from=str(my_timestrp_from.time())
                str_to=str(my_timestrp_to.time())
            #Segunda casuistica, 2 pm to 3 pm
            if x==0:
                from_time=time_refined1[0:1]+':00 '+ time_refined1[2:4]
                to_time=time_refined1[-4:-3]+':00 '+ time_refined1[-2:]
                my_timestrp_from = datetime.strptime(from_time, format)
                my_timestrp_to = datetime.strptime(to_time, format)
                str_from=str(my_timestrp_from.time())
                str_to=str(my_timestrp_to.time())
            #Segunda casuistica, 2:30 pm to 3 pm or 2:00 to 3:30 pm
            if x==1:
                if time_refined1[1]==":":
                    from_time=time_refined1[0:7]
                    to_time=time_refined1[-4:-3]+':00 '+ time_refined1[-2:]
                    my_timestrp_from = datetime.strptime(from_time, format)
                    my_timestrp_to = datetime.strptime(to_time, format)
                    str_from=str(my_timestrp_from.time())
                    str_to=str(my_timestrp_to.time())
                else:
                    from_time=time_refined1[0:1]+':00 '+ time_refined1[2:4]
                    to_time=time_refined1[-7:]
                    my_timestrp_from = datetime.strptime(from_time, format)
                    my_timestrp_to = datetime.strptime(to_time, format)
                    str_from=str(my_timestrp_from.time())
                    str_to=str(my_timestrp_to.time())

    return  str_from, str_to


def identify_action(text_speech):
    list_tokens, list_ent = parsing(text_speech)
    verbs = searching_verb(list_tokens)
    return verbs

# This should go out! (the following things I mean)

#MAIN CALLS
#_____________________________________________
sentence=speech_recognition()
[list_tags, list_ents]=parsing(sentence)
print(list_ents)
#First state
verb=searching_verb(list_tags)
print(verb)
#Second state
print(list_ents[0][1])
when=searching_date(list_ents)
print(when)
#Third state
#Tiempo formato string
from_time,to_time=searching_time(list_ents)
print ( from_time+" to "+to_time)
#_____________________________________________
