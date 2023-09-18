from controllers.db_connection import get_db


def get_event(event_id):
    with get_db().cursor() as cursor:
        cursor.execute('''  SELECT
                                *
                            FROM events
                            WHERE event_id = %s; ''', event_id)
        event = cursor.fetchone()
        event['start'] = event['start_datetime'].strftime('%H:%M')
        event['end'] = event['end_datetime'].strftime('%H:%M')
        event['date'] = event['start_datetime'].strftime('%d/%m/%Y')
        return event


def sign_event(event_id, teacher_id, user_id, signature):
    with get_db().cursor() as cursor:
        cursor.execute('''  INSERT INTO signatures (event_id, teacher_id, user_id, signature_svg, signature_datetime)
                            VALUES (%s, %s, %s, %s, NOW()); ''', (event_id, teacher_id, user_id, signature))
        get_db().commit()


def to_sign_events(session, date=None):
    with get_db().cursor() as cursor:
        list_id = session['signature_list']
        if list_id is None:
            return []
        else:
            if date is not None:
                cursor.execute('''SELECT *
                                FROM events
                                WHERE list_id = %s AND DATE(start_datetime) = %s AND (hidden = FALSE OR hidden IS NULL)
                                ORDER BY start_datetime DESC;''', (list_id, date))
            else:
                cursor.execute('''SELECT *
                              FROM events
                              LEFT JOIN signatures s ON events.event_id = s.event_id AND s.user_id = %s
                              WHERE list_id = %s AND start_datetime < NOW() AND s.signature_id IS NULL AND (hidden = FALSE OR hidden IS NULL)
                              ORDER BY start_datetime DESC;''', (session['user_id'], list_id))

            events = cursor.fetchall()
            for event in events:
                event['start'] = event['start_datetime'].strftime('%H:%M')
                event['end'] = event['end_datetime'].strftime('%H:%M')
                event['date'] = event['start_datetime'].strftime('%d/%m/%Y')
            return events


# TODO : refactor and light this function
def get_history(user_id):
    cursor = get_db().cursor()
    cursor.execute(''' SELECT *, 
                              CONCAT(DATE(start_datetime), ' ', ADDTIME(TIME(start_datetime), '02:00:00'), ' - ', ADDTIME(TIME(end_datetime), '02:00:00')) AS date,
                              CONCAT(DATE(signature_datetime), ' à ', ADDTIME(TIME(signature_datetime), '02:00:00')) AS date_signature,
                              t.teacher_name AS signataire
                       FROM events
                       LEFT JOIN signatures s ON events.event_id = s.event_id
                        LEFT JOIN teachers t ON s.teacher_id = t.teacher_id
                       WHERE s.signature_id IS NOT NULL AND user_id = %s
                       ORDER BY start_datetime DESC
                       LIMIT 50;
                       ''', user_id)
    return cursor.fetchall()


def abs_event(event_id, user_id):
    with get_db().cursor() as cursor:
        cursor.execute('''  DELETE FROM signatures WHERE user_id = %s AND event_id = %s; ''', (user_id, event_id))
        cursor.execute('''  INSERT INTO signatures (event_id, user_id, signature_datetime, signature_svg, teacher_id)
                            VALUES (%s, %s, NOW(), 'ABSENT', NULL); ''', (event_id, user_id))
        get_db().commit()


def del_sign(id):
    with get_db().cursor() as cursor:
        cursor.execute('''  DELETE FROM signatures
                            WHERE signature_id = %s; ''', id)
        get_db().commit()


def sign_many(event_id, teacher_id, students, signature):
    with get_db().cursor() as cursor:
        for student in students:
            cursor.execute('''  INSERT INTO signatures (event_id, teacher_id, user_id, signature_svg, signature_datetime)
                                VALUES (%s, %s, %s, %s, NOW()); ''', (event_id, teacher_id, student, signature))
        get_db().commit()


def del_event(id):
    with get_db().cursor() as cursor:
        cursor.execute('''  UPDATE events SET hidden=TRUE WHERE event_id = %s; ''', id)
        get_db().commit()
