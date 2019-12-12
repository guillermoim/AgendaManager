import pandas as pd


#TODO: The following function goes out

def indetify_action(input):
    return 'add'


class Appointment():

    '''
        Esta clase sirve para tener los Appointments como objetos en Python y
        poder operar con ellos de forma fácil.
    '''

    def __init__(self, date = None, startTime = None, endTime = None, subject = None ,tags = None, priority = None):
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.subject = subject
        self.tags = tags
        self.priority = priority

def import_agenda(path_to_agenda):
    '''Dado el path de la agenda, lo devuelve como un DataFrame de Pandas'''
    return pd.read_csv(path_to_agenda)

def conflict_appointments(agenda, new_appointment):
    '''
        Here what I check are two conditions:
        1) That there is no appointment in the agenda in the same date with a startTime
        before the new app start time and that ends later than the new app starts
        2 )That there is no appointment in the agenda in the same date with a startTime
        adter the new app start time and whose startTime is later than the new appointment
        starts.
    '''
    res = agenda[((agenda.date == new_appointment.date) &
    (agenda.startTime <= new_appointment.startTime) &
    (agenda.endTime >= new_appointment.startTime)) |
    (agenda.date == new_appointment.date) &
    (agenda.startTime >= new_appointment.startTime) &
    (agenda.startTime <= new_appointment.endTime) ]

    return df_to_list(res)


def filter_by_date(agenda, start_date, end_date):
    return agenda[(agenda.date>=start_date) & (agenda.date <= end_date)]

def filter_by_tags(agenda, tag):
    return agenda[agenda.tags.str.contains(tag)]

def appointment_to_pd(a):
    cols = ['date','startTime','endTime','subject','tags','priority']
    return pd.DataFrame([[a.date, a.startTime, a.endTime, a.subject, a.tags, a.priority]], columns = cols)

def add_appointment(agenda, appointment):
    res = appointment_to_pd(appointment)
    print(res)
    return agenda.append(res, ignore_index = True)

def update_agenda(agenda, file):
    agenda.to_csv(file, index = False)

def pd_to_appointment(df_row):
    return Appointment(df_row.date, df_row.startTime, df_row.endTime, df_row.subject, df_row.tags, df_row.priority)

def df_to_list(df):

    res = []

    for index, row in df.iterrows():
        aux = pd_to_appointment(row)
        res.append(aux)

    return res
