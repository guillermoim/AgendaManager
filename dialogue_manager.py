import agenda_manager as AM
import generation as gen
import asr_parser as parser
from colorama import Fore
import TTS

def main():
    # Global variables
    state = None
    conflict = None
    new_appointment = None
    file = 'agenda.csv'
    agenda = AM.import_agenda(file)

    # Stop Condition to exit the while loop. We use directly after the input with an if (not needed).
    #stop_condition = False

    vengine = TTS.init_engine()

    first_line = 'Welcome to your agenda manager!'
    print('MACHINE: '+first_line)
    TTS.read(vengine, first_line)

    flag_first_conflict = True

    while(True):

        # First identify the state of the converstation
        if state == None:
            output = 'What do you want to do?'
            print('MACHINE: ' + output)
            TTS.read(vengine, output)
            # TODO: Read the outputs with TTS
            input = parser.speech_recognition()
            print('YOU: '+input)
            op = parser.identify_action(input)

            if op == 'add':
                state = 'add'
                new_appointment = AM.Appointment()
                parser.fill_new_appointment(new_appointment, input)
                continue
            elif op == 'query':
                state = 'query'
            elif op == 'rmv':
                state == 'rmv'
            elif input=='stop':
                print("Thanks for using your favourite agenda manager. Good bye!")
                break
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
                print('YOU: '+input)
                if input=='stop':
                    print("Thanks for using your favourite agenda manager. Good bye!")
                    break
                date = parser.searching_date(input)
                if date == '':
                    output = 'Sorry, I did not hear a date!'
                    print('MACHINE: '+output)
                    TTS.read(vengine, output)
                else:
                    new_appointment.date = date
                

            # If the start time is empty ask for the start time
            if new_appointment.startTime is None:
                output = 'What time will it start?'
                print('MACHINE: '+output)
                TTS.read(vengine, output)
                input = parser.speech_recognition()
                print('YOU: '+input)
                if input=='stop':
                    print("Thanks for using your favourite agenda manager. Good bye!")
                    break
                startTime = parser.get_simple_time(input)
                if startTime == '':
                    output = 'I am sorry, I expect you to say a time!'
                    print('MACHINE: '+output)
                    TTS.read(vengine, output)
                else:
                    new_appointment.startTime = startTime
                continue

            # If the end time is empty ask for the end time
            if new_appointment.endTime is None:
                output = 'What time will it end?'
                print('MACHINE: '+output)
                TTS.read(vengine, output)
                input = parser.speech_recognition()
                print('YOU: '+input)
                if input=='stop':
                    print("Thanks for using your favourite agenda manager. Good bye!")
                    break
                endTime = parser.get_simple_time(input)
                if endTime == '':
                    output = 'I am sorry, I expect you to say a time!'
                    print('MACHINE: '+output)
                    TTS.read(vengine, output)
                else:
                    new_appointment.endTime = endTime
                continue

            # HERE IMPORTANT!! CHECK FOR CONFLICTIVE APPOINTMENTS
            # Switch to conflict state!
            conflict = AM.conflict_appointments(agenda, new_appointment)
            if  len(conflict) > 0:
                output = gen.conflict_appointments(len(conflict))
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
                print('YOU: '+input)
                new_appointment.subject = input

            # If there are no tags?
            if new_appointment.tags is None:
                output = 'Do you want to add any tags?'
                print('MACHINE: '+output)
                TTS.read(vengine, output)
                input = parser.speech_recognition()
                print('YOU: '+input)
                if input=='stop':
                    print("Thanks for using your favourite agenda manager. Good bye!")
                    break

                aux = parser.is_aff_or_neg(input)

                if aux == 'AFF':
                    parsed = parser.parsing(input)
                    verb, verb_idx = parser.get_verb_idx(parsed[0])
                    tags = parser.detect_tags(parsed[0], verb_idx)
                    new_appointment.tags = tags
                    if len(tags) < 1:
                        output = 'Which ones?'
                        TTS.read(vengine, output)
                        print('MACHINE: '+output)
                        input = parser.speech_recognition()
                        print('YOU: '+input)
                        if input=='stop':
                            print("Thanks for using your favourite agenda manager. Good bye!")
                            break
                        parsed = parser.parsing(input)
                        verb, verb_idx = parser.get_verb_idx(parsed[0])
                        tags = parser.detect_tags(parsed[0], verb_idx)
                        new_appointment.tags = tags

                elif aux == 'NEG':
                    tags = ''
                    new_appointment.tags = tags
                elif aux == 'CLARIFY':
                    output = 'Sorry you have to decide if you want to add any tag'
                    print('MACHINE: '+output)
                    TTS.read(vengine, output)
                elif aux == 'SPECIFY':
                    pass

            # If priority is empty?
            if new_appointment.priority is None:
                output = 'Is this appointment important?'
                print('MACHINE: '+output)
                TTS.read(vengine, output)
                input = parser.speech_recognition()
                print('YOU: '+input)
                if input=='stop':
                    print("Thanks for using your favourite agenda manager. Good bye!")
                    break
                aux = parser.is_aff_or_neg(input)
                if aux == 'NEG':
                    new_appointment.priority = 'low'
                elif aux == 'AFF':
                    output = 'Very important?'
                    print('MACHINE: '+output)
                    TTS.read(vengine, output)
                    input = parser.speech_recognition()
                    print('YOU: '+input)
                    if input=='stop':
                        print("Thanks for using your favourite agenda manager. Good bye!")
                        break
                    aux = parser.is_aff_or_neg(input)
                    if aux == 'NEG':
                        new_appointment.priority = 'med'
                    elif aux == 'AFF':
                        new_appointment.priority = 'high'


            agenda = AM.add_appointment(agenda, new_appointment)
            AM.update_agenda(agenda, file)
            output = gen.appointment_saved(new_appointment)
            print('MACHINE: '+ output)
            TTS.read(vengine, output)
            state = None
            new_appointment = None
            conflict = None
            continue

        if state == 'conflict':

            if flag_first_conflict:
                output = gen.read_conflict(AM.df_to_list(conflict))
                print('MACHINE: '+ output)
                TTS.read(vengine, output)

            output = 'Do you want to overwrite the existing appointments or reschedule the new one?'
            print('MACHINE: '+ output)
            TTS.read(vengine, output)

            input = parser.speech_recognition()
            print('YOU: '+input)
            if input=='stop':
                print("Thanks for using your favourite agenda manager. Good bye!")
                break
            aux = parser.reschedule_or_overwrite(input)

            if aux == 'reschedule':
                new_appointment.date = None
                new_appointment.startTime = None
                new_appointment.endTime = None

                state = 'add'
                conflict = None

                flag_first_conflict = True

                continue

            elif aux == 'overwrite':
                agenda = AM.remove_apps_from_agenda(agenda, conflict)
                AM.update_agenda(agenda, file)

                state = 'add'
                conflict = None

                flag_first_conflict = True

                continue

            else:
                output = 'Sorry, I did not understand you'
                print('MACHINE: '+ output)
                TTS.read(vengine, output)
                flag_first_conflict = False
                continue


        if state == 'query':
            output = gen.read_appointments(agenda)
            print('MACHINE: '+ output)
            TTS.read(vengine, output)


            state = None

        if state == 'rmv':
            # TODO
            pass

        if state == 'error':
            output = 'Sorry I cannot help you with that.'
            print('MACHINE: '+ output)
            TTS.read(vengine, output)
            state = None
            continue
        #Not needed, we use the break after the input.
        #if stop_condition:
            #break
