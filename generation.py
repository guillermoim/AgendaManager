def appointment_saved(app):
    res = 'Okay! I have saved an appointment the ' + str(app.date) \
    + ' from ' + str(app.startTime) + ' to ' + str(app.endTime) \
    + ' with subject '+ str(app.subject)
    return res

def conflict_appointments(quantity):
    aux = 'appointment'
    if quantity > 1:
        aux+='s'
    res = 'Watch out! You have ' + str(quantity)+ ' '+ aux \
        + ' conflicting with the timeslot specified.'

    return res

def read_conflict(conflict):
    s = ''
    if len(conflict) > 1:
        s+='The conflictive appointments are \n'
    else:
        s+='The conflictive appointment is \n'

    for idx, app in enumerate(conflict):
        if idx < len(conflict)-2:
            s+=read_appointment(app)+',\n'
        if idx == len(conflict)-2:
            s+=read_appointment(app)+' and \n'
        elif idx == len(conflict)-1:
            s+=read_appointment(app)

    return s

def read_appointment(app):
    s=''
    s+=app.subject+' '+app.date +' from '+app.startTime+' to '+ app.endTime
    return s
