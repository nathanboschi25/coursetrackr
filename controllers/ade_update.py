from flask import Blueprint

from models.events.AdeDAO import update_events_from_ade
from models.signature_list import ListeDAO

ade_update = Blueprint('ade_update', __name__, template_folder='views')

@ade_update.route('/update_all')
def update_all():
    for list in ListeDAO.get_listes():
        update_events_from_ade(list['list_id'])
    return "ok"