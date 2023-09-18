from datetime import datetime

import requests
from ics import Calendar

from controllers.db_connection import get_db


def get_ade_events(list_id):
    with get_db().cursor() as cursor:
        cursor.execute("SELECT url_ical FROM signature_list WHERE list_id = %s", list_id)
    r = requests.get(cursor.fetchone()['url_ical'])
    c = Calendar(r.text)

    events = []
    for event in c.events:
        events.append({
            'uid': event.uid,
            'start_datetime': event.begin.datetime,
            'end_datetime': event.end.datetime,
            'title': event.name,
            'content': event.description
        })
    return events


def update_events_from_ade(list_id, force=False):
    if list_id is None:
        return
    # on regarde deja les evenements futurs connus dans la base de données
    with get_db().cursor() as cursor:
        cursor.execute("SELECT uid_ade FROM events WHERE list_id = %s", list_id)
        known_events = cursor.fetchall()
        known_events = [event['uid_ade'] for event in known_events]

        for ade_event in get_ade_events(list_id):
            if ade_event['uid'] not in known_events and ade_event['start_datetime'] > datetime.now(ade_event['start_datetime'].tzinfo) or force:
                cursor.execute(
                    "INSERT INTO events (uid_ade, start_datetime, end_datetime, title, content, list_id) VALUES (%s, ADDTIME(%s, '02:00:00'), ADDTIME(%s, '02:00:00'), %s, %s, %s)",
                    (ade_event['uid'], ade_event['start_datetime'], ade_event['end_datetime'], ade_event['title'],
                     ade_event['content'][2:200], list_id))
                get_db().commit()
            else:
                if ade_event['start_datetime'] < datetime.now(ade_event['start_datetime'].tzinfo):
                    continue
                cursor.execute(
                    "UPDATE events SET start_datetime = ADDTIME(%s, '02:00:00'), end_datetime = ADDTIME(%s, '02:00:00'), title = %s, content = %s WHERE uid_ade = %s AND list_id = %s;",
                    (ade_event['start_datetime'], ade_event['end_datetime'], ade_event['title'],
                     ade_event['content'][2:200], ade_event['uid'], list_id))
                get_db().commit()
