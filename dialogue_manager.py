 import agenda_manager as AM
import generation as gen
import parser
from colorama import Fore
import TTS

def main():
    # Global variables
    state = None
    old_appointment = None
    new_appointment = None
    file = 'agenda.csv'
    agenda = AM.import_agenda(file)

    first_flag = True

    # Stop Condition to exit the while loop
    stop_condition = False

    vengine = TTS.init_engine()

    first_line = 'Welcome to your agenda manager!'
    print('MACHINE: '+first_line)
    TTS.read(vengine, first_line)

    while(True):

        # First identify the state of the converstation
        if state == None:
            output = 'What do you want to do?'
            print('MACHINE: ' + output)
            TTS.read(vengine, output)
            # TODO: Read the outputs with TTS
            input = parser.speech_recognition()
            print(input)
            op = AM.identify_action(input) # This function is NOT well implented and it should not be in that module

            if op == 'add':
                state = 'add'
                new_appointment = AM.Appointment()
                parser.fill_new_appointment(new_appointment, input)
                continue
            elif op == 'query':
                state = 'query'
            elif op == 'rmv':
                state == 'rmv'
            elif op == 'error':
                state = 'error'

        # If the state of the conversation has been identified as
        # adding a new appointment
        if state == 'add':
            # If the date is empty ask for the date
            if new_appointment.date is None:
                output = 'Which day will it be?'
                print('MACHINE: '+output)
                TTS.read(vengine, output)
                input = parser.speech_recognition()
                date = parser.searching_date(input)
                if date == '':
                    print('Sorry, I did not hear a date!')
                    continue
                else:
                    new_appointment.date = date

            # If the start time is empty ask for the start time
            if new_appointment.startTime is None:
                output = 'What time will it start?'
                print('MACHINE: '+output)
                TTS.read(vengine, output)
                input = parser.speech_recognition()
                startTime = parser.get_simple_time(input)
                if startTime == '':
                    print('I am sorry, I expect you to say a time!')
                else:
                    new_appointment.startTime = startTime
                continue

            # If the end time is empty ask for the end time
            if new_appointment.endTime is None:
                output = 'What time will it end?'
                print('MACHINE: '+output)
                TTS.read(vengine, output)
                input = parser.speech_recognition()
                print(input)
                endTime = parser.get_simple_time(input)
                if endTime == '':
                    print('I am sorry, I expect you to say a time!')
                else:
                    new_appointment.endTime = endTime
                continue

            # HERE IMPORTANT!! CHECK FOR CONFLICTIVE APPOINTMENTS
            # Switch to conflict state!
            conf = len(AM.conflict_appointments(agenda, new_appointment))
            if  conf > 0:
                output = gen.conflict_appointments(conf)
                print('MACHINE: '+output)
                TTS.read(vengine, output)
                state = 'conflict'
                continue

            # If the subject is empty...
            if new_appointment.subject is None:
                output = 'What is the subject of the appointment?'
                print('MACHINE: '+output)
                TTS.read(vengine, output)
                input = parser.speech_recognition()
                print(input)
                new_appointment.subject = input

            # If there are no tags?
            if new_appointment.tags is None:
                output = 'Do you want to add any tags?'
                print('MACHINE: '+output)
                TTS.read(output)
                input = parser.speech_recognition()
                print(input)
                answer, tags = parser.[]()
                pass

            # If priority is empty?
            if new_appointment.priority is None:
                # TODO:
                pass

            agenda = AM.add_appointment(agenda, new_appointment)
            AM.update_agenda(agenda, file)
            output = gen.appointment_saved(new_appointment)
            print('MACHINE: '+ output)
            TTS.read(vengine, output)
            state = None
            continue

        if state == 'conflict':
            print('CONFLICTIVE')
            break
            pass

        if state == 'error':
            output = 'Sorry I cannot help you with that.'
            print('MACHINE: '+ output)
            TTS.read(vengine, output)

        if stop_condition:
            break


    print(Fore.WHITE)
