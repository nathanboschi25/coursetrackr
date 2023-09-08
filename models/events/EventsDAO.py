from datetime import datetime

from controllers.db_connection import get_db


def get_event(event_id):
    with get_db().cursor() as cursor:
        cursor.execute('''  SELECT
                                event_id,
                                DATE(start_datetime) AS date,
                                TIME(start_datetime) AS start,
                                TIME(end_datetime) AS end,
                                title,
                                content
                            FROM events
                            WHERE event_id = %s; ''', event_id)
        return cursor.fetchone()


def sign_event(event_id, teacher_id, user_id, signature):
    with get_db().cursor() as cursor:
        cursor.execute('''  INSERT INTO signatures (event_id, teacher_id, user_id, signature_svg, signature_datetime)
                            VALUES (%s, %s, %s, %s, NOW()); ''', (event_id, teacher_id, user_id, signature))
        get_db().commit()


def to_sign_events(user_id):
    with get_db().cursor() as cursor:
        cursor.execute('''SELECT list_id FROM users WHERE user_id = %s;''', user_id)
        list_id = cursor.fetchone()['list_id']
        if list_id is None:
            return []
        else:
            cursor.execute('''SELECT *,
                              CONCAT(DATE(start_datetime), ' ', TIME(start_datetime), ' - ', TIME(end_datetime)) AS date
                              FROM events
                              LEFT JOIN signatures s ON events.event_id = s.event_id
                              WHERE start_datetime < NOW() AND s.sinature_id IS NULL AND list_id = %s
                              ORDER BY start_datetime DESC;''', list_id)
            return cursor.fetchall()


def get_history(user_id):
    cursor = get_db().cursor()
    cursor.execute(''' SELECT *, 
                              CONCAT(DATE(start_datetime), ' ', ADDTIME(TIME(start_datetime), '02:00:00'), ' - ', ADDTIME(TIME(end_datetime), '02:00:00')) AS date,
                              CONCAT(DATE(signature_datetime), ' à ', ADDTIME(TIME(signature_datetime), '02:00:00')) AS date_signature,
                              t.teacher_name AS signataire
                       FROM events
                       LEFT JOIN signatures s ON events.event_id = s.event_id
                        LEFT JOIN teachers t ON s.teacher_id = t.teacher_id
                       WHERE s.sinature_id IS NOT NULL AND user_id = %s
                       ORDER BY start_datetime DESC;
                       ''', user_id)
    return cursor.fetchall()
