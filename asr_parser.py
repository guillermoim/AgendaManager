import speech_recognition as sr
import spacy
from spacy import displacy
from pathlib import Path
from datetime import datetime
from datetime import timedelta
import re
from collections import Counter

def speech_recognition():
    # obtain audio from the microphone
    print('\t(Listening...)')
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
        text_speech=r.recognize_google(audio)
        #print("Google Speech Recognition thinks you said: " + text_speech)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return text_speech


def parsing(text_speech):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text_speech)
   # Second structure, entities with displacy.render. Type in your web search--> http://127.0.0.1:"number of port given"/
    #POS: The simple part-of-speech tag.
    #Tag: The detailed part-of-speech tag.
    list_tokens=[("Tokens", "Lemma", "Pos", "Dependencies", "Tags")]
    list_ent=[]
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

    #print_full_information(list_tokens)
    return list_tokens, list_ent

def print_full_information(list_tokens):
    for Text, Lemma, Position, Tag, Dependency in list_tokens:
        print(f"{Text:{20}} {Lemma:{20}} {Position:{20}} {Tag:{20}} {Dependency:{20}}")

#1 FIRST STATE:  verbs like ADD, CANCEL, INFO
def searching_verb(text):

    list_tokens, list_ent = parsing(text)

    cnt=0
    idx = None
    verbs_tokens=[]
    for item in list_tokens:
        #Add or delete can be written with another verb that can be ROOT, therefore we take into account 'xcomp' as: I want to add an appointment.
        if item[-2]=='xcomp' or  item[-2]=='ROOT' and item[-3] in ('VERB'):
            idx = cnt
            verbs_tokens.append(item)
            cnt+=1
    #Number to return the corresponding row of the proper token. Watch out cnt+=1
    if len(verbs_tokens) > 0:
        return verbs_tokens[idx][1]
    else:
        return ''

#2 SECOND STATE: dates like 25th December, next Monday etc (IN DEVELOPMENT)
def searching_date(text):

    list_tokens, list_ent = parsing(text)
    #In case we have more entities we are picking only DATE! For the next states we will pick "TIME" or cardinal.
    weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    month_list=['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']

    if list_tokens:
        for text, ent in list_ent:
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
                        #We sum up the days until next appointment to the actual date
                        sum_day=timedelta(days=d)
                        new_date=now+sum_day
                        #We put it in the format we want.
                        date_output=datetime.strftime(new_date, '%Y-%m-%d')#%d/%m/%Y
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
                            date_output=datetime.strftime(date_current_year, '%Y-%m-%d')
                        #CASE 3: 25th of February 2020
                        else:
                            date_proposed_year=datetime(int(date_intro[-1]), index_month, int(date_intro[0]), 0, 0)
                            date_output=datetime.strftime(date_proposed_year, '%Y-%m-%d')
                    #CASE 4 TOMORROW
                    if n=="tomorrow":
                        tomorrow_days=timedelta(days=1)
                        tomorrow=now+tomorrow_days
                        date_output=datetime.strftime(tomorrow, '%Y-%m-%d')
                    #CASE 5 TODAY
                    if n=="today":
                        date_output=datetime.strftime(now, '%Y-%m-%d')
            return date_output
    else:
        return ''

def searching_time(text):

    list_tokens, list_ent = parsing(text)

    count = 0
    idx = None

    res = ''

    if list_tokens:
        for text, ent in list_ent:
            #We take into account only the DATE entity
            if ent=="TIME":
                idx = count
                break
            count+=1

    #When there is no entity
    if idx == None:
        res = ''
    else:
        res = list_ent[idx]

    return res

def get_simple_time(text):
    time_ent = searching_time(text)
    if time_ent=='':
        return ''
    else:
        return get_from_to_time(time_ent)[0]

def get_from_to_time(time_entity):
    text = time_entity[0]
    parts = text.split('to')
    from_time = get_time(parts[0])
    to_time = ''
    if len(parts) > 1:
        to_time = get_time(parts[1])
    return from_time, to_time

def get_time(time_string):
    time = time_string.strip()
    time_splitted = time.split(' ')
    return format_time(time_splitted[-2], time_splitted[-1])

def format_time(time, period):
    time = time.split(':')
    res = ''

    if period == 'a.m.':
        if len(time) > 1:
            hour = '{:02d}'.format(int(time[0]))
            if hour == '12':
                hour = '00'
            min = time[1]
            res = hour+':'+min
        else:
            hour = '{:02d}'.format(int(time[0]))
            if hour == '12':
                hour = '00'
            min = '00'
            res = hour+':'+min

    elif period == 'p.m.':
        if len(time) > 1:
            hour = str(int('{:02d}'.format(int(time[0]))) + 12)
            if hour == '24':
                hour = '12'
            min = time[1]
            res = hour+':'+min
        else:
            hour = str(int('{:02d}'.format(int(time[0]))) + 12)
            if hour == '24':
                hour = '12'
            min = '00'
            res = hour+':'+min

    return res

def fill_new_appointment(app, text):
    date = searching_date(text)
    times = searching_time(text)
    startTime = ''
    endTime = ''

    if times != '':
        startTime, endTime = get_from_to_time(times)

    if date != '':
        app.date = date
    if startTime != '':
        app.startTime = startTime
    if endTime != '':
        app.endTime = endTime

def get_verb_idx(list_tokens):
    cnt = 0
    idx = None
    for item in list_tokens:
        #Add or delete can be written with another verb that can be ROOT, therefore we take into account 'xcomp' as: I want to add an appointment.
        if item[-2]=='xcomp' or item[-2]=='ROOT' and item[-3] in ('VERB', 'AUX'):
            idx = cnt
            #verbs_tokens.append(item)
        cnt+=1
    #Number to return the corresponding row of the proper token. Watch out cnt+=1
    if idx != None:
        return list_tokens[idx][1], idx
    else:
        return '', idx

def affirmative_and_tags(text_speech):
    list_tokens, list_ent = parsing(text_speech)
    verb, idx = get_verb_idx(list_tokens)

    tokens_len = len(list_tokens)

    affirmative = is_affirmative(text_speech)

    if verb != '':
        pass
    else:
        pass

    return verb

def detect_tags(list_tokens, verb_idx):
    res = []
    if verb_idx is None:
        for i in range(1, len(list_tokens)):
            token = list_tokens[i]
            pos = token[2]
            if pos in ('ADJ', 'NOUN'):
                res.append(token[0])
    else:
        for i in range(verb_idx+1, len(list_tokens)):
            token = list_tokens[i]
            pos = token[2]
            if pos in ('ADJ', 'NOUN'):
                res.append(token[0])

    return ':'.join(res)

def is_aff_or_neg(text):
    res1 = is_affirmative(text)
    res2 = is_negation(text)

    res = ''

    if res1 and not res2:
        res = 'AFF'
    elif not res1 and res2:
        res = 'NEG'
    elif not res1 and not res2:
        res = 'SPECIFY'
    elif res1 and res1:
        res = 'CLARIFY'

    return res

def is_affirmative(text):
    affirmative_words = ['yes', 'sure']
    res = []
    for word in affirmative_words:
        idx = text.find(word)
        res.append(idx)

    res = [it >= 0 for it in res]
    return any(res)

def is_negation(text):
    negation_words = ['no']
    res = []
    for word in negation_words:
        idx = text.find(word)
        res.append(idx)

    res = [it >= 0 for it in res]
    return any(res)

def identify_action(text_speech):
    adding_verbs = ('add', 'create')
    query_verbs = ('tell', 'know', 'get', 'search', 'display', 'show')
    delete_verbs = ('delete', 'remove', 'clear')

    verb = searching_verb(text_speech)

    if verb in adding_verbs:
        res = 'add'
    elif verb in query_verbs:
        res = 'query'
    elif verb in delete_verbs:
        res = 'rmv'
    else:
        res = 'error'

    return res

def reschedule_or_overwrite(text):
    re_verbs = ('reschedule', 'rearrage')
    over_verbs = ('overwrite', 'replace')

    verb = searching_verb(text)

    res = ''

    if verb in re_verbs:
        res = 'reschedule'
    elif verb in over_verbs:
        res = 'overwrite'

    return res
