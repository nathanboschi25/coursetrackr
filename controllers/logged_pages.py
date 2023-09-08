from flask import Blueprint, url_for, render_template, redirect, session, flash

from controllers.db_connection import get_db
from models.events import EventsDAO, AdeDAO
from models.signature_list import ListeDAO
from models.teachers.TeachersDAO import extract_teacher
from models.users import UsersDAO

connected = Blueprint('connected', __name__)


@connected.before_request
def before_request():
    if 'username' not in session:
        print("someone tried to access a connected page without being connected")
        return redirect(url_for('auth_security.auth_login'))
    with get_db().cursor() as cursor:
        cursor.execute('''SELECT * FROM users WHERE username=%s''', session['username'])
        user = cursor.fetchone()
        if user is None:
            session.clear()
            return redirect(url_for('auth_security.auth_login'))
        session['user_id'] = user['user_id']
        session['name'] = user['name']
        session['username'] = user['username']


@connected.route('/dashboard')
def dashboard():
    a_signer = EventsDAO.to_sign_events(session['user_id'])
    return render_template('dashboard/index.html', user=session, a_signer=a_signer, get_prof=extract_teacher)

@connected.route('/dashboard/get_events_from_ade')
def get_events_from_ade():
    AdeDAO.update_events_from_ade(UsersDAO.get_user(session['user_id'])['list_id'])
    flash("Les évènements ont été mis à jour")
    return redirect(url_for('connected.dashboard'))

@connected.route('/settings')
def settings():
    return render_template('dashboard/settings.html', compte=UsersDAO.get_user(session['user_id']), listes=ListeDAO.get_listes())

from controllers.events import events
connected.register_blueprint(events, url_prefix='/events')

from controllers.admin import admin
connected.register_blueprint(admin, url_prefix='/admin')

from controllers.pdf_generator import generate_document
connected.register_blueprint(generate_document, url_prefix='/gen')
