from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session

from models.events import EventsDAO
from models.users import UsersDAO
from models.teachers import TeachersDAO

events = Blueprint('events', __name__, template_folder='views')


@events.route('/')
def history():
    return render_template('events/history.html', signatures=EventsDAO.get_history(session['user_id']))


@events.route('/sign/<int:id>', methods=['GET'])
def ask_sign(id):
    event = EventsDAO.get_event(id)
    if event:
        return render_template('events/sign.html', event=event, teachers=TeachersDAO.get_teachers())
    flash('Event not found', 'error')
    return redirect(url_for('dashboard'))

@events.route('/sign/<int:id>', methods=['POST'])
def sign(id):
    event = EventsDAO.get_event(id)

    if not request.form['teacher']:
        flash('Please enter all the fields', 'error')
    else:
        EventsDAO.sign_event(id, request.form['teacher'], session['user_id'],
                                    request.form['signature'])
        flash('Record was successfully added')
        return redirect(url_for('connected.dashboard'))
