import datetime

from flask import Blueprint, session, redirect, url_for, render_template, request, flash

from models.events import EventsDAO
from models.signature_list import ListeDAO

teachers = Blueprint('teachers', __name__, template_folder='views')


@teachers.before_request
def before_request():
    if 'teacher_id' not in session:
        print("someone tried to access a secured page without being connected")
        session.clear()
        return redirect(url_for('auth_security.auth_login'))


@teachers.route('/dashboard')
def dashboard():
    date = request.args.get('date') if request.args.get('date') else datetime.date.today()
    cours = EventsDAO.to_sign_events(session, date=date)
    return render_template('teachers/dashboard.html', user=session, date=date, cours=cours)


@teachers.route('/sign/<int:id>', methods=['GET'])
def sign(id):
    event = EventsDAO.get_event(id)
    if event:
        return render_template('teachers/sign.html', event=event,
                               students=ListeDAO.get_students(session['signature_list']), user=session)
    flash('Event not found', 'error')
    return redirect(url_for('teachers.dashboard'))


@teachers.route('/sign/<int:id>', methods=['POST'])
def sign_post(id):
    print(request.form.getlist('students'))
    EventsDAO.sign_many(id, session['teacher_id'], request.form.getlist('students'), request.form['signature'])
    return redirect(url_for('teachers.dashboard'))
