from controllers.db_connection import get_db


def get_listes():
    with get_db().cursor() as cursor:
        cursor.execute(
            '''SELECT CONCAT(annee_univ, ' | ', designation) AS designation, list_id, url_ical, annee_univ FROM signature_list;''')
        return cursor.fetchall()
