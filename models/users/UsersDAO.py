from controllers.db_connection import get_db

def get_user(user_id):
    with get_db().cursor() as cursor:
        cursor.execute('''SELECT * FROM users WHERE user_id = %s;''', user_id)
        return cursor.fetchone()