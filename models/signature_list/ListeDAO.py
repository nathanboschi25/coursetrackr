from controllers.db_connection import get_db


def get_listes():
    with get_db().cursor() as cursor:
        cursor.execute(
            '''SELECT CONCAT(annee_univ, ' | ', designation) AS designation, list_id, url_ical, annee_univ FROM signature_list;''')
        return cursor.fetchall()


def get_students(list_id):
    with get_db().cursor() as cursor:
        cursor.execute(
            '''SELECT * FROM users WHERE list_id=%s ORDER BY name''', list_id)
        return cursor.fetchall()
