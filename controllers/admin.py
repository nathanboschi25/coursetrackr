from flask import Blueprint, request, flash, redirect, url_for

from models.events import EventsDAO
from models.teachers import TeachersDAO

admin = Blueprint('admin', __name__, template_folder='views')

@admin.route('/teachers/add', methods=['POST'])
def add_teacher():
    if not request.form['name']:
        flash('Please enter all the fields', 'error')
    else:
        TeachersDAO.add_teacher(request.form['name'])
        flash('Record was successfully added')
    return redirect(url_for('connected.settings'))

@admin.route('/event/del/<int:event_id>', methods=['GET'])
def del_event(event_id):
    EventsDAO.del_event(event_id)
    return redirect(url_for('connected.dashboard'))
