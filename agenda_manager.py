import pandas as pd


#TODO: The following function goes out

def indetify_action(input):
    return 'add'


class Appointment():

    '''
        Esta clase sirve para tener los Appointments como objetos en Python y
        poder operar con ellos de forma fácil.
    '''

    def __init__(self, date = None, startTime = None, endTime = None, subject = None ,tags = [], priority = 'low'):
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
    return agenda[((agenda.date == new_appointment.date) &
    (agenda.startTime <= new_appointment.startTime) &
    (agenda.endTime >= new_appointment.startTime)) |
    (agenda.date == new_appointment.date) &
    (agenda.startTime >= new_appointment.startTime) &
    (agenda.startTime <= new_appointment.endTime) ]


def filter_by_date(agenda, start_date, end_date):
    return agenda[(agenda.date>=start_date) & (agenda.date <= end_date)]

def filter_by_tags(agenda, tag):
    return agenda[agenda.tags.str.contains(tag)]

def appointment_to_pd(a):
    return pd.DataFrame([a.date, a.startTime, a.endTime, a.subject, a.tags, a.priority])

def add_appointment(agenda, appointment):
    res = appointment_to_pd(appointment)
    agenda.append(res, ignoreIndex = True)

def update_agenda(agenda, file):
    agenda.to_csv(file)


# Funciones de testeo muy cutronas!
def test1():
    print('Sloppy Testing with both cases')

    file = 'agenda.csv'
    agenda = import_agenda(file)

    print('Here I create an agenda with an existing appointment \
    the 2019-12-06 from 13:30:00 to 14:00:00')

    print('Case 1: A new appointment the same date from 13:45:00 to 13:50:00')
    app = Appointment(date='2019-12-06', startTime='13:45:00', endTime='14:50:00')
    print('\n\t CONFLICTIVE EXISTING APPOINTMENTS:')
    print(conflict_appointments(agenda, app))

    print('Case 2: A new appointment the same date from 13:15:00 to 13:50:00')
    app = Appointment(date='2019-12-06', startTime='13:15:00', endTime='14:50:00')
    print('\n\t CONFLICTIVE EXISTING APPOINTMENTS:')
    print(len(conflict_appointments(agenda, app)))

def test2():
    print('Sloppy Testing with both cases')
    file = 'agenda.csv'
    agenda = import_agenda(file)

    print(filter_by_tags(agenda, 'important').to_numpy())

def test3():
    app = Appointment(date='2019-12-08', startTime='13:45:00',
    endTime='14:50:00', subject = 'Test 2')
    print('')


if __name__ == '__main__':

    test1()
    #test2()
