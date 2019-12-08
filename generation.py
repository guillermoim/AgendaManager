def appointment_saved(app):
    res = 'Okay! I have saved an appointment the ' + str(app.date) \
    + ' from ' + str(app.startTime) + ' to ' + str(app.endTime) \
    + ' with subject '+ str(app.subject)

    return res
