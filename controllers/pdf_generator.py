import base64
from datetime import datetime, timedelta

from flask import render_template, url_for, redirect, request, flash, session, send_file, Blueprint, make_response
import pdfkit

from models.pdf.GetDataDAO import get_data

generate_document = Blueprint('generate_document', __name__)


@generate_document.route('/', methods=['GET'])
def choose_generation():
    return render_template('document/index.html')


@generate_document.route('/', methods=['POST'])
def ask_generation():
    date = datetime.strptime(request.form.get('date'), "%Y-%m-%d")
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)

    start = str(start).split(' ')[0]
    end = str(end).split(' ')[0]

    pdf_options = {'encoding': 'UTF-8',
                   'margin-left': '3mm',
                   'margin-right': '3mm',
                   'margin-bottom': '3mm',
                   'margin-top': '3mm',
                   'Title': ('Fiche d\'emargement - Semaine du ' + start + ' au ' + end)}

    if request.form.get('export') == 'pdf':
        html = render_template('document/pdf.html', len=len,
                               donnees=get_data(session['user_id'], start, end))
        pdf = pdfkit.from_string(html, False, options=pdf_options)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=fiche_emargement_' + session[
            'name'] + '_' + start + '_' + end + '.pdf'
        return response
    else:
        return render_template('document/pdf.html', len=len,
                               donnees=get_data(session['user_id'], start, end))


@generate_document.route('/html')
def render_html():
    start = '2023-09-04'
    end = '2023-09-10'
    return render_template('document/pdf.html', len=len,
                           donnees=get_data(session['user_id'], start, end))
