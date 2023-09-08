from controllers.db_connection import get_db


def get_teachers():
    with get_db().cursor() as cursor:
        cursor.execute('SELECT * FROM teachers ORDER BY teacher_name')
        return cursor.fetchall()


def get_teachers_names():
    with get_db().cursor() as cursor:
        cursor.execute('SELECT teacher_name FROM teachers ORDER BY teacher_name')
        teachers_names = []
        for teacher in cursor.fetchall():
            teachers_names.append(teacher['teacher_name'])
        return teachers_names

def extract_teacher(content):
    content = content.split('\n')
    for line in content:
        if line in get_teachers_names():
            return line
    return '-'


def add_teacher(name):
    with get_db().cursor() as cursor:
        cursor.execute('INSERT INTO teachers(teacher_name) VALUES (%s)', name)
        get_db().commit()
