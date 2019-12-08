import agenda_manager as AM
import generation as gen
import parser
from colorama import Fore

def main():
    # Global variables
    state = None
    old_appointment = None
    new_appointment = None
    file = 'agenda.csv'
    agenda = AM.import_agenda(file)


    # Stop Condition to exit the while loop
    stop_condition = False

    first_line = 'Welcome to your agenda manager!'
    # read(first_line)

    while(True):

        # First identify the state of the converstation
        if state == None:
            output = 'What do you want to do?'
            print(Fore.BLUE + output)
            # TODO: Read the outputs with TTS
            input = parser.speech_recognition()
            print(Fore.RED + output)
            # op = identify_action(input) ?
            op = 'add'
            if op == 'add':
                state = 'add'
                new_appointment = AM.Appointment()
                # fill_new_appointment(new_appointment, input)
                new_appointment.date = '2019-12-07'
                new_appointment.startTime = '14:30:00'
                new_appointment.endTime = '15:30:00'
                continue

        # If the state of the conversation has been identified as
        # adding a new appointment
        if state == 'add':
            # If the date is empty ask for the date
            if new_appointment.date is None:
                print(Fore.BLUE+'When will it be?')
                input = parser.speech_recognition()
                #date = obtain_date(input)
                new_appointment.date = date

            # If the start time is empty ask for the start time
            if new_appointment.startTime is None:
                print(Fore.BLUE+'What time will it start?')
                input = parser.speech_recognition()
                print(Fore.RED+input)
                # startTime = obtain_time(input)
                new_appointment.startTime = startTime

            # If the end time is empty ask for the end time
            if new_appointment.endTime is None:
                print(Fore.BLUE+'What time will it end?')
                input = parser.speech_recognition()
                print(Fore.RED+input)
                # endTime = obtain_time(input)
                new_appointment.endTime = endTime

            # HERE IMPORTANT!! CHECK FOR CONFLICTIVE APPOINTMENTS
            # Switch to conflict state!
            if len(AM.conflict_appointments(agenda, new_appointment)) > 0:
                print(Fore.BLUE+'Watch out! There are some existing appointments that conflict \
                with the date and time specified.')
                state = 'conflict'
                continue

            # If the subject is empty...
            if new_appointment.subject is None:
                print(Fore.BLUE+'What is the subject of the appointment?')
                input = parser.speech_recognition()
                print(Fore.RED+input)
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
            print(Fore.BLUE+output)
            state = None
            print(Fore.WHITE)

        if state == 'conflict':
            print('CONFLICTIVE')
            break
            pass

        if stop_condition:
            break


    print()
