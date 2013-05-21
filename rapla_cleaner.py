from flask import Flask, request
import requests
import re

app = Flask(__name__)


def split_vevents(input):
    in_event_data = False
    event_data = ""
    for line in input.splitlines():
        if line == 'BEGIN:VEVENT':
            event_data = ""
            in_event_data = True

        if in_event_data:
            event_data += line + "\r\n"

        if line == 'END:VEVENT':
            in_event_data = False
            yield event_data


@app.route("/")
def clean():

    if 'user' not in request.args:
        return "Missing Rapla User"
    elif 'file' not in request.args:
        return "Missing Rapla Filename"

    r = requests.get(
        'http://rapla.dhbw-karlsruhe.de/rapla?page=iCal&user=%s&file=%s' %
        (request.args['user'], request.args['file'])
    )
    data, events = r.text.split('BEGIN:VEVENT', 1)

    for event in split_vevents(events):
        if re.findall(r'SUMMARY:.*?(Z).*?', event) and \
           'without_z_courses' in request.args:
            continue

        if 'EXDATE' in event:
            tz, t = re.findall(r'DTSTART;TZID=(.*?):\d+T(\d+)', event)[0]
            data += re.sub(
                r"EXDATE;VALUE=DATE:(\d+)",
                "EXDATE;TZID=" + tz + ":\g<1>T" + t,
                event
            )
        else:
            data += event

    data += "END:VCALENDAR\r\n"

    res = app.make_response(data)
    res.mimetype = "text/calendar"
    return res

if __name__ == "__main__":
    app.run(debug=True)
