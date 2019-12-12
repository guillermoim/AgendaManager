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
