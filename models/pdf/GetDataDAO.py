from datetime import datetime

from controllers.db_connection import get_db
from models.teachers.TeachersDAO import get_teachers_names, extract_teacher


def get_data(user_id, semaine_start, semaine_end):
    with get_db().cursor() as cursor:
        cursor.execute('''      SELECT 
                                    signature_list.annee_univ,
                                    users.name,
                                    signature_list.designation
                                FROM users
                                LEFT JOIN signature_list ON users.list_id = signature_list.list_id
                                WHERE users.user_id = %s;''', user_id)
        result = cursor.fetchone()
        return {
            'annee_universitaire': result['annee_univ'],
            'etudiant': {
                'name': result['name'],
                'classe': result['designation']
            },
            'semaine': {
                'start': semaine_start,
                'end': semaine_end,
                'jours': get_jours(user_id, semaine_start, semaine_end)
            }
        }


def get_user_list(user_id):
    with get_db().cursor() as cursor:
        cursor.execute('SELECT list_id FROM users WHERE user_id=%s', user_id)
        return cursor.fetchone()['list_id']


def get_cours(user_id, jour):
    with get_db().cursor() as cursor:
        cursor.execute('''
                        SELECT
                            ev.*,
                            s.*,
                            t.teacher_name
                        FROM events ev
                        LEFT JOIN signatures s ON ev.event_id = s.event_id
                        LEFT JOIN teachers t ON t.teacher_id = s.teacher_id
                        WHERE DATE(start_datetime) = %s AND ev.list_id = %s
                        ORDER BY start_datetime; 
                        ''', (jour, get_user_list(user_id)))
        results = cursor.fetchall()
        cours = []
        for result in results:
            cours.append({
                'start': result['start_datetime'].time().isoformat(timespec='minutes'),
                'end': result['end_datetime'].time().isoformat(timespec='minutes'),
                'title': result['title'],
                'teacher': extract_teacher(result['content']),
                'signature_svg': result['signature_svg'],
                'signature_name': result['teacher_name'],
                'signature_date': result['signature_datetime'],
                'now': {
                    'date': datetime.now().strftime('%m/%d/%Y'),
                    'heure': datetime.now().time().isoformat(timespec='minutes')
                }
            })
        return cours


def get_jours(user_id, semaine_start, semaine_end):
    with get_db().cursor() as cursor:
        cursor.execute('''
                            SELECT DISTINCT
                                DATE(start_datetime) AS date
                            FROM signature_list sl
                            JOIN events ev ON sl.list_id = ev.list_id
                            WHERE
                                sl.list_id = %s AND
                                ev.start_datetime >= %s AND
                                ev.end_datetime <= %s
                            ORDER BY start_datetime
                            ''', (get_user_list(user_id), semaine_start, semaine_end))
        jours = []
        for date in cursor.fetchall():
            jour = date['date']
            jours.append({
                'jour': jour.strftime('%A'),
                'date': jour.strftime('%m/%d/%Y'),
                'cours': get_cours(user_id, jour)
            })
        return jours
