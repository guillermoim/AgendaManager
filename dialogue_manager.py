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
            op = 'add' #AM.identify_action(input) # This function is NOT well implented and it should not be in that module
            if op == 'add':
                state = 'add'
                new_appointment = AM.Appointment()
                parser.fill_new_appointment(new_appointment, input)
                continue

        # If the state of the conversation has been identified as
        # adding a new appointment
        if state == 'add':
            # If the date is empty ask for the date
            if new_appointment.date is None:
                print('MACHINE: '+'When will it be?')
                input = parser.speech_recognition()
                #date = obtain_date(input)
                new_appointment.date = date

            # If the start time is empty ask for the start time
            if new_appointment.startTime is None:
                print('MACHINE: '+'What time will it start?')
                input = parser.speech_recognition()
                print(input)
                # startTime = obtain_time(input)
                new_appointment.startTime = startTime

            # If the end time is empty ask for the end time
            if new_appointment.endTime is None:
                print('MACHINE: '+'What time will it end?')
                input = parser.speech_recognition()
                print(input)
                # endTime = obtain_time(input)
                new_appointment.endTime = endTime

            # HERE IMPORTANT!! CHECK FOR CONFLICTIVE APPOINTMENTS
            # Switch to conflict state!
            if len(AM.conflict_appointments(agenda, new_appointment)) > 0:
                print('MACHINE: '+'Watch out! There are some existing appointments that conflict \
                with the date and time specified.')
                state = 'conflict'
                continue

            # If the subject is empty...
            if new_appointment.subject is None:
                print('MACHINE: '+'What is the subject of the appointment?')
                input = parser.speech_recognition()
                print(input)
                new_appointment.subject = input

            # If there are no tags?
            if len(new_appointment.tags) == 0:
                # TODO:
                pass

            # If priority is empty?
            if priority is None:
                # TODO:
                pass

            AM.add_appointment(agenda, new_appointment)
            output = gen.appointment_saved(new_appointment)
            print('MACHINE: '+output)
            state = None

        if state == 'conflict':
            print('CONFLICTIVE')
            break
            pass

        if stop_condition:
            break


    print(Fore.WHITE)
